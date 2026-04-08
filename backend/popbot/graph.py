"""LangGraph deterministic-routing agent for PopBot (Rasa-inspired).

Architecture: LLM understands, code routes.
Linear graph: guardrail → classify → execute_tool → respond → finalize → END
No tool bindings on the LLM. No loops possible.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Annotated, AsyncGenerator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from .classifier import classify, SlotContext, BookingSlots, resolve_next_weekday
from .llm_classifier import classify_with_llm
from .observability import get_langfuse_handler
from .prompts import build_system_prompt, LA_POP_NAILS_SYSTEM_PROMPT
from .tools import (
    get_services_data, get_available_dates_data,
    get_time_slots_data, lookup_client_data, start_booking_action,
    init_tools,
    # Booking slot-filling helpers
    match_service, derive_schedule, format_date_es,
    validate_booking_date, validate_booking_time,
    get_available_dates_for_booking, get_time_slots_for_booking,
    lookup_client_record, SERVICE_PRICES,
    # Memory
    get_client_memory, save_conversation_memory,
)

import os


# In-memory slot context per session
_session_slots: dict[str, SlotContext] = {}

# Off-topic signals for the guardrail
OFF_TOPIC_SIGNALS = [
    "politica", "futbol", "programa", "hackea", "ignora instrucciones",
    "ignore instructions", "olvida tus instrucciones", "eres chatgpt",
    "eres gpt", "prompt injection",
]

CANNED_REJECTION = (
    "Solo puedo ayudarte con informacion sobre La Pop Nails. "
    "Te gustaria saber sobre nuestros servicios o agendar una cita?"
)


class PopBotState(TypedDict):
    messages: Annotated[list, add_messages]
    session_id: str
    frontend_action: dict | None
    intent: str
    entities: dict
    tool_result: str
    tool_name: str
    client_memory: dict | None


# ── Node 1: Guardrail ──────────────────────────────────────────────

def guardrail(state: PopBotState) -> PopBotState:
    """Check if the latest message is in scope."""
    last_msg = state["messages"][-1]
    if not isinstance(last_msg, HumanMessage):
        return state

    text = last_msg.content.lower()
    matched = [s for s in OFF_TOPIC_SIGNALS if s in text]
    if matched:
        print(f"[PopBot] Guardrail BLOCKED: '{text}' matched: {matched}")
        return {
            **state,
            "messages": [AIMessage(content=CANNED_REJECTION)],
        }
    print(f"[PopBot] Guardrail PASSED: '{text}'")
    return state


def after_guardrail(state: PopBotState) -> str:
    """Route after guardrail: if blocked, skip to finalize."""
    last = state["messages"][-1]
    if isinstance(last, AIMessage):
        return "finalize"
    return "classify"


# ── Node 2: Intent Classification ──────────────────────────────────

async def classify_intent(state: PopBotState) -> PopBotState:
    """Classify intent: regex fast path, LLM fallback for off_topic."""
    last_msg = state["messages"][-1]
    if not isinstance(last_msg, HumanMessage):
        return {**state, "intent": "off_topic", "entities": {}}

    text = last_msg.content
    session_id = state.get("session_id", "")
    slot_ctx = _session_slots.get(session_id, SlotContext())

    # Fast path: regex
    result = classify(text, slot_ctx)

    # LLM fallback: only when regex says off_topic
    if result.intent == "off_topic":
        llm_result = await classify_with_llm(text)
        if llm_result.intent != "off_topic":
            # Merge any regex-extracted entities with LLM entities
            merged_entities = {**result.entities, **llm_result.entities}
            result = llm_result
            result.entities = merged_entities
            print(f"[PopBot] LLM override: '{text}' -> {result.intent}")

    # Safety net: if booking is active, override to booking_continue
    # (catches cases where LLM fallback returned something unexpected)
    if slot_ctx.booking.active and result.intent not in (
        "cancel_booking", "ask_services", "ask_availability",
        "ask_time_slots", "book", "booking_continue",
    ):
        print(f"[PopBot] Booking override: '{text}' {result.intent} -> booking_continue")
        result.intent = "booking_continue"

    print(f"[PopBot] Classified: '{text}' -> intent={result.intent}, entities={result.entities}")

    return {
        **state,
        "intent": result.intent,
        "entities": result.entities,
        "tool_result": "",
        "tool_name": "",
    }


# ── Node 3: Execute Tool ──────────────────────────────────────────

async def execute_tool(state: PopBotState) -> PopBotState:
    """Execute the right tool based on classified intent. One tool per turn."""
    intent = state.get("intent", "")
    entities = state.get("entities", {})
    session_id = state.get("session_id", "")
    slot_ctx = _session_slots.get(session_id, SlotContext())

    tool_result = ""
    tool_name = ""
    frontend_action = state.get("frontend_action")

    if intent == "ask_services":
        tool_name = "get_services"
        tool_result = await get_services_data()

    elif intent == "ask_availability":
        tool_name = "get_available_dates"
        tool_result = await get_available_dates_data()

    elif intent == "ask_time_slots":
        date = entities.get("date", "")
        if not date and entities.get("weekday") is not None:
            date = resolve_next_weekday(entities["weekday"])
        if date:
            tool_name = "get_time_slots"
            tool_result = await get_time_slots_data(date)
        else:
            tool_name = "get_time_slots"
            tool_result = "NEED_DATE"

    elif intent == "lookup":
        phone = entities.get("phone", "")
        if phone:
            tool_name = "lookup_client"
            tool_result = await lookup_client_data(phone)
            memory = await get_client_memory(phone)
            if memory:
                state = {**state, "client_memory": memory}
        else:
            tool_name = "lookup_client"
            tool_result = "NEED_PHONE"

    elif intent in ("book", "booking_continue"):
        tool_name = "booking_flow"
        booking = slot_ctx.booking

        if not booking.active:
            booking.active = True

        # Get raw user text for field-specific interpretation
        last_msg = state["messages"][-1]
        raw_text = last_msg.content if isinstance(last_msg, HumanMessage) else ""

        # Fill slots from extracted entities
        _fill_booking_slots(booking, entities, raw_text)

        # Phone provided? Auto-lookup client + load memory
        if booking.phone and not booking.client_found:
            client = await lookup_client_record(booking.phone)
            if client:
                booking.client_found = True
                booking.name = booking.name or client.get("name", "")
                booking.email = booking.email or client.get("email", "")
                # Load client memory for personalization
                memory = await get_client_memory(booking.phone)
                if memory:
                    state = {**state, "client_memory": memory}
                print(f"[PopBot] Client found: {booking.name}")

        # Find what's still missing
        missing = _get_missing_booking_fields(booking)

        if not missing:
            # All fields collected → open wizard at payment step
            frontend_action = {
                "action": "OPEN_WIZARD_PAYMENT",
                "params": {
                    "name": booking.name,
                    "phone": booking.phone,
                    "email": booking.email,
                    "service": booking.service,
                    "date": booking.date,
                    "time": booking.time,
                    "step": "5",
                },
            }
            tool_result = json.dumps({"booking_status": "complete"})
            booking.active = False
            print(f"[PopBot] Booking complete: {booking.name} {booking.service} {booking.date} {booking.time}")
        else:
            next_field = missing[0]
            booking.awaiting_field = next_field
            field_data = await _get_booking_field_context(next_field, booking)
            tool_result = json.dumps({
                "booking_status": "collecting",
                "next_field": next_field,
                "field_data": field_data,
                "greeting": booking.client_found and booking.name and next_field != "phone",
            })
            print(f"[PopBot] Booking: next={next_field}, filled={_booking_filled_count(booking)}/7")

    elif intent == "cancel_booking":
        tool_name = "booking_flow"
        slot_ctx.booking = BookingSlots()
        tool_result = json.dumps({"booking_status": "cancelled"})

    elif intent == "followup":
        if slot_ctx.last_tool_result:
            tool_name = slot_ctx.last_tool_name
            tool_result = slot_ctx.last_tool_result
        elif slot_ctx.last_intent:
            # Re-run the previous intent's tool
            return await _rerun_last_intent(state, slot_ctx)

    # greet, off_topic: no tool call, LLM handles directly

    # Update slot context
    if tool_result and tool_result not in ("NEED_DATE", "NEED_PHONE"):
        slot_ctx.last_intent = intent
        slot_ctx.last_tool_result = tool_result
        slot_ctx.last_tool_name = tool_name
    elif intent not in ("followup",):
        slot_ctx.last_intent = intent
    _session_slots[session_id] = slot_ctx

    if tool_name:
        print(f"[PopBot] Tool: {tool_name} → {len(tool_result)} chars")

    return {
        **state,
        "tool_result": tool_result,
        "tool_name": tool_name,
        "frontend_action": frontend_action,
    }


# ── Booking Slot-Filling Helpers ──────────────────────────────────

def _fill_booking_slots(booking: BookingSlots, entities: dict, raw_text: str):
    """Fill booking slots from entities and raw text based on awaiting_field."""
    import re

    clean = raw_text.strip()

    # When awaiting service, try to match service FIRST from raw text
    # This prevents bare digits like "2" from being misinterpreted as times
    service_matched_from_text = False
    if booking.awaiting_field == "service" and not booking.service:
        matched = match_service(clean)
        if matched:
            booking.service = matched
            service_matched_from_text = True

    # Fill from extracted entities
    if entities.get("phone") and not booking.phone:
        booking.phone = entities["phone"]
    if entities.get("email") and not booking.email:
        booking.email = entities["email"]

    # Resolve weekday to date if no explicit date
    if not entities.get("date") and entities.get("weekday") is not None:
        entities["date"] = resolve_next_weekday(entities["weekday"])

    if entities.get("date"):
        validation = validate_booking_date(entities["date"])
        if validation["valid"]:
            booking.date = entities["date"]
        else:
            booking.date_rejection = validation["error"]

    # Skip time extraction if this turn was a service selection (bare digit like "2")
    if entities.get("time") and entities["time"] not in ("morning", "afternoon") and not service_matched_from_text:
        if booking.date:
            validation = validate_booking_time(entities["time"], booking.date)
            if validation["valid"]:
                booking.time = entities["time"]
                booking.schedule = derive_schedule(entities["time"])
            else:
                booking.time_rejection = validation["error"]
        else:
            booking.time = entities["time"]
            booking.schedule = derive_schedule(entities["time"])

    # Try to match service from entities (if not already matched from raw text)
    if not booking.service:
        service_entity = entities.get("service", "")
        if service_entity:
            matched = match_service(service_entity)
            if matched:
                booking.service = matched

    if booking.awaiting_field == "name" and not booking.name:
        # Strip common prefixes
        name = re.sub(r"^(me\s*llamo|soy|mi\s*nombre\s*es)\s*", "", clean, flags=re.IGNORECASE).strip()
        if name and len(name) >= 2:
            booking.name = name.title()

    if booking.awaiting_field == "email" and not booking.email:
        email_match = re.search(r"[\w.-]+@[\w.-]+\.\w{2,}", clean)
        if email_match:
            booking.email = email_match.group(0)

    if booking.awaiting_field == "phone" and not booking.phone:
        phone_match = re.search(r"\d{10}", clean)
        if phone_match:
            booking.phone = phone_match.group(0)

    if booking.awaiting_field == "confirm":
        confirm_words = {"si", "sí", "ok", "dale", "listo", "va", "confirmo", "yes"}
        if clean.lower().strip("!. ") in confirm_words:
            # Mark as confirmed by setting awaiting_field to done
            booking.awaiting_field = "confirmed"


def _get_missing_booking_fields(booking: BookingSlots) -> list[str]:
    """Return list of missing fields in priority order."""
    missing = []
    if not booking.phone:
        missing.append("phone")
    if not booking.service:
        missing.append("service")
    if not booking.date:
        missing.append("date")
    if not booking.time:
        missing.append("time")
    if not booking.email:
        missing.append("email")
    if not booking.name:
        missing.append("name")
    # If all fields present, need confirmation
    if not missing and booking.awaiting_field != "confirmed":
        missing.append("confirm")
    return missing


def _booking_filled_count(booking: BookingSlots) -> int:
    """Count how many booking fields are filled."""
    count = 0
    for field in [booking.phone, booking.service, booking.date, booking.time, booking.email, booking.name]:
        if field:
            count += 1
    if booking.awaiting_field == "confirmed":
        count += 1
    return count


async def _get_booking_field_context(field: str, booking: BookingSlots) -> str:
    """Get contextual data to help the user fill a specific field."""
    if field == "date":
        dates = await get_available_dates_for_booking()
        if dates:
            formatted = [format_date_es(d) for d in dates]
            return ", ".join(formatted)
        return "No hay fechas disponibles proximamente."

    if field == "time":
        slots = await get_time_slots_for_booking(booking.date)
        parts = []
        if slots["morning"]:
            parts.append(f"Manana: {', '.join(slots['morning'])}")
        if slots["afternoon"]:
            parts.append(f"Tarde: {', '.join(slots['afternoon'])}")
        return " | ".join(parts) if parts else "No hay horarios disponibles para esa fecha."

    if field == "confirm":
        price = SERVICE_PRICES.get(booking.service, "?")
        date_fmt = format_date_es(booking.date) if booking.date else booking.date
        return json.dumps({
            "service": booking.service,
            "price": price,
            "date": date_fmt,
            "time": booking.time,
            "name": booking.name,
            "email": booking.email,
        })

    return ""


def _build_booking_prompt(next_field: str, field_data: str, booking: BookingSlots) -> str:
    """Build deterministic Spanish prompt for the next booking field."""
    if next_field == "phone":
        return "Claro! Para agendar necesito tu numero de telefono (10 digitos)."

    if next_field == "service":
        prefix = ""
        if booking.client_found and booking.name:
            prefix = f"Hola {booking.name}! Que gusto verte de nuevo. "
        return (
            f"{prefix}Que servicio te interesa? Todos incluyen manicura.\n"
            "1. Nivelacion en una natural - $500 + diseno (3h-3h30)\n"
            "2. Refuerzo con tecnica hibrida - $600 + diseno (3h30-4h)\n"
            "3. Extension hibrida - $700 + diseno (4h-4h15)\n"
            "Puedes decirme el numero o el nombre."
        )

    if next_field == "date":
        rejection = booking.date_rejection
        if rejection:
            booking.date_rejection = ""  # Clear after using
            if field_data:
                return f"{rejection} Fechas disponibles: {field_data}"
            return f"{rejection} Que dia te gustaria?"
        if field_data:
            return f"Que dia te gustaria? Fechas disponibles: {field_data}"
        return "Que dia te gustaria para tu cita?"

    if next_field == "time":
        date_fmt = format_date_es(booking.date) if booking.date else booking.date
        rejection = booking.time_rejection
        if rejection:
            booking.time_rejection = ""  # Clear after using
            if field_data:
                return f"{rejection} Horarios disponibles para {date_fmt}: {field_data}"
            return f"{rejection} Que hora te gustaria para el {date_fmt}?"
        if field_data:
            return f"A que hora? Horarios para {date_fmt}: {field_data}"
        return f"A que hora te gustaria para el {date_fmt}?"

    if next_field == "email":
        return "Cual es tu correo electronico? Lo necesitamos para enviarte la confirmacion."

    if next_field == "name":
        return "A que nombre agendamos la cita?"

    if next_field == "confirm":
        try:
            data = json.loads(field_data)
            return (
                f"Tu cita quedaria asi:\n"
                f"Servicio: {data['service']} (${data['price']} MXN)\n"
                f"Fecha: {data['date']}\n"
                f"Hora: {data['time']}\n"
                f"Nombre: {data['name']}\n\n"
                f"El anticipo es de $250 MXN. Confirmas? (si/no)"
            )
        except (json.JSONDecodeError, KeyError):
            return "Confirmas tu cita? (si/no)"

    return "Continuemos con tu reserva."


async def _rerun_last_intent(state: PopBotState, slot_ctx: SlotContext) -> PopBotState:
    """Re-run the tool from the previous intent for followup."""
    rerun_state = {**state, "intent": slot_ctx.last_intent, "entities": {}}
    return await execute_tool(rerun_state)


# ── Node 4: LLM Response ──────────────────────────────────────────

def _get_llm():
    """Get LLM instance with NO tool bindings."""
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=512,
        api_key=os.environ.get("GROQ_API_KEY"),
    )


async def respond(state: PopBotState) -> PopBotState:
    """Generate natural language response with tool data in context."""
    tool_result = state.get("tool_result", "")
    messages = state["messages"]

    llm = _get_llm()

    # Build response messages
    system_content = state.get("_system_prompt", LA_POP_NAILS_SYSTEM_PROMPT)
    response_messages = [SystemMessage(content=system_content)]

    # Add conversation history
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage)):
            response_messages.append(msg)

    # Deterministic responses — skip LLM for simple slot-filling prompts
    intent = state.get("intent", "")
    session_id = state.get("session_id", "")
    slot_ctx = _session_slots.get(session_id, SlotContext())

    # Booking flow: all responses are deterministic
    if intent in ("book", "booking_continue"):
        try:
            parsed = json.loads(tool_result)

            if parsed.get("booking_status") == "complete":
                summary = _build_booking_prompt(
                    "confirm",
                    json.dumps({
                        "service": slot_ctx.booking.service if slot_ctx.booking.active else "",
                        "price": "?",
                    }),
                    slot_ctx.booking,
                )
                msg = "Perfecto! Te abro el formulario de pago para completar tu reserva."
                print(f"[PopBot] booking complete → deterministic")
                return {"messages": [AIMessage(content=msg)]}

            if parsed.get("booking_status") == "collecting":
                next_field = parsed["next_field"]
                field_data = parsed.get("field_data", "")
                msg = _build_booking_prompt(next_field, field_data, slot_ctx.booking)
                print(f"[PopBot] booking ask={next_field} → deterministic")
                return {"messages": [AIMessage(content=msg)]}

        except (json.JSONDecodeError, KeyError) as e:
            print(f"[PopBot] booking parse error: {e}")

    if intent == "cancel_booking":
        msg = "No hay problema! Si cambias de opinion, aqui estoy para ayudarte."
        print("[PopBot] cancel_booking → deterministic")
        return {"messages": [AIMessage(content=msg)]}

    if tool_result == "NEED_DATE":
        print("[PopBot] NEED_DATE → deterministic response (skip LLM)")
        return {"messages": [AIMessage(
            content="Claro! Para checar horarios necesito saber que dia te interesa. Que fecha tienes en mente?"
        )]}
    elif tool_result == "NEED_PHONE":
        print("[PopBot] NEED_PHONE → deterministic response (skip LLM)")
        return {"messages": [AIMessage(
            content="Para buscar tu historial necesito tu numero de telefono. Me lo compartes?"
        )]}

    # Inject client memory for personalization
    client_memory = state.get("client_memory")
    if client_memory and client_memory.get("name"):
        mem_parts = [f"CLIENTE CONOCIDA: {client_memory['name']}"]
        if client_memory.get("appointment_count"):
            mem_parts.append(f"Citas previas: {client_memory['appointment_count']}")
        if client_memory.get("last_service"):
            mem_parts.append(f"Ultimo servicio: {client_memory['last_service']}")
        if client_memory.get("preferred_schedule"):
            mem_parts.append(f"Horario preferido: {client_memory['preferred_schedule']}")
        memory_injection = "\n".join(mem_parts)
        response_messages.append(SystemMessage(
            content=f"[MEMORIA DE CLIENTE - Usa esta info para personalizar tu respuesta de forma natural. "
                    f"No listes estos datos, solo intégralos naturalmente]:\n{memory_injection}"
        ))

    # Inject tool data as mandatory context
    if tool_result:
        injection = (
            f"\n\n[DATOS OBTENIDOS - DEBES incluir esta informacion COMPLETA en tu respuesta. "
            f"No digas 'obtuve los datos'. Presenta la informacion directamente al usuario]:\n"
            f"{tool_result}"
        )
        response_messages.append(SystemMessage(content=injection))

    try:
        response = await llm.ainvoke(response_messages)
        print(f"[PopBot] LLM response: {response.content[:100] if response.content else 'empty'}")
        return {"messages": [response]}
    except Exception as e:
        print(f"[PopBot] LLM error: {e}")
        # Fallback: return raw tool data or error message
        if tool_result:
            return {"messages": [AIMessage(content=tool_result)]}
        return {"messages": [AIMessage(
            content="Disculpa, estoy teniendo problemas tecnicos. Por favor intenta de nuevo."
        )]}


# ── Node 5: Finalize ──────────────────────────────────────────────

def finalize(state: PopBotState) -> PopBotState:
    """Final pass — state is already complete."""
    return state


# ── Graph Construction ─────────────────────────────────────────────

def build_graph():
    """Build the linear 5-node graph. No loops."""
    graph = StateGraph(PopBotState)

    graph.add_node("guardrail", guardrail)
    graph.add_node("classify", classify_intent)
    graph.add_node("execute_tool", execute_tool)
    graph.add_node("respond", respond)
    graph.add_node("finalize", finalize)

    graph.set_entry_point("guardrail")
    graph.add_conditional_edges("guardrail", after_guardrail, {
        "classify": "classify",
        "finalize": "finalize",
    })
    graph.add_edge("classify", "execute_tool")
    graph.add_edge("execute_tool", "respond")
    graph.add_edge("respond", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()


# Singleton compiled graph
_compiled_graph = None


def get_graph():
    """Get or build the compiled graph singleton."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


# ── Streaming Entry Point ──────────────────────────────────────────

async def stream_popbot(
    message: str,
    history: list[dict],
    session_id: str | None = None,
    db=None,
    tenant_id: str = "",
) -> AsyncGenerator[str, None]:
    """Stream PopBot responses as SSE-formatted events."""
    session_id = session_id or str(uuid.uuid4())

    if db is not None:
        init_tools(db, tenant_id)

    try:
        graph = get_graph()
        system_prompt = await build_system_prompt(db, tenant_id)

        # Build message history
        messages = []
        for msg in (history or [])[-10:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            elif role == "assistant":
                messages.append(AIMessage(content=content))
        messages.append(HumanMessage(content=message))

        input_state = {
            "messages": messages,
            "session_id": session_id,
            "frontend_action": None,
            "intent": "",
            "entities": {},
            "tool_result": "",
            "tool_name": "",
            "client_memory": None,
            "_system_prompt": system_prompt,
        }

        # Langfuse tracing
        langfuse_handler = get_langfuse_handler(session_id=session_id)
        config = {"callbacks": [langfuse_handler]} if langfuse_handler else {}

        # Stream events from LangGraph
        full_response = ""
        tool_event_emitted = False
        # Capture metadata for rich conversation logging
        _captured_intent = ""
        _captured_entities = {}
        _captured_tool_name = ""
        _captured_tool_result = ""
        _captured_frontend_action = None

        # JSON prefix sanitizer: Groq models sometimes output classifier
        # JSON (e.g. {"intent": "greet", ...}) before the actual response.
        # Buffer initial tokens and strip any leading JSON blob.
        _json_buf = ""
        _json_state = "checking"  # "checking" → "stripping" → "streaming"

        async for event in graph.astream_events(input_state, config=config, version="v2"):
            kind = event["event"]

            # LLM token streaming
            if kind == "on_chat_model_stream":
                chunk = event["data"].get("chunk")
                if chunk and chunk.content:
                    token = chunk.content
                    if isinstance(token, str) and token:
                        # JSON prefix sanitizer state machine
                        if _json_state == "checking":
                            _json_buf += token
                            stripped = _json_buf.lstrip()
                            if stripped.startswith("{"):
                                _json_state = "stripping"
                            elif len(_json_buf) > 3 or (stripped and not stripped[0] in "{"):
                                # Not JSON — flush buffer normally
                                _json_state = "streaming"
                                full_response += _json_buf
                                yield f"data: {json.dumps({'type': 'token', 'content': _json_buf})}\n\n"
                                _json_buf = ""
                        elif _json_state == "stripping":
                            _json_buf += token
                            # Look for end of JSON object (closing braces)
                            brace_depth = 0
                            end_pos = -1
                            for i, ch in enumerate(_json_buf):
                                if ch == "{":
                                    brace_depth += 1
                                elif ch == "}":
                                    brace_depth -= 1
                                    if brace_depth == 0:
                                        end_pos = i + 1
                                        break
                            if end_pos > 0:
                                # Strip JSON prefix, yield any remaining text
                                remaining = _json_buf[end_pos:].lstrip()
                                _json_state = "streaming"
                                print(f"[PopBot] Stripped JSON prefix: {_json_buf[:end_pos][:60]}...")
                                if remaining:
                                    full_response += remaining
                                    yield f"data: {json.dumps({'type': 'token', 'content': remaining})}\n\n"
                                _json_buf = ""
                            elif len(_json_buf) > 300:
                                # Safety: if buffer too large, just flush everything
                                _json_state = "streaming"
                                full_response += _json_buf
                                yield f"data: {json.dumps({'type': 'token', 'content': _json_buf})}\n\n"
                                _json_buf = ""
                        else:
                            # Normal streaming
                            full_response += token
                            yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"

            # Detect execute_tool completion to emit tool events
            elif kind == "on_chain_end" and not tool_event_emitted:
                output = event.get("data", {}).get("output", {})
                if isinstance(output, dict):
                    t_name = output.get("tool_name", "")
                    t_result = output.get("tool_result", "")
                    f_action = output.get("frontend_action")
                    t_intent = output.get("intent", "")
                    t_entities = output.get("entities", {})

                    # Capture metadata for logging
                    if t_intent:
                        _captured_intent = t_intent
                    if t_entities:
                        _captured_entities = t_entities

                    if t_name and not tool_event_emitted:
                        _captured_tool_name = t_name
                        _captured_tool_result = t_result
                        yield f"data: {json.dumps({'type': 'tool_call', 'tool': t_name})}\n\n"
                        if t_result and t_result not in ("NEED_DATE", "NEED_PHONE"):
                            yield f"data: {json.dumps({'type': 'tool_result', 'tool': t_name, 'result': t_result})}\n\n"
                        tool_event_emitted = True

                    if f_action and f_action.get("action"):
                        _captured_frontend_action = f_action
                        yield f"data: {json.dumps({'type': 'action', 'action': f_action['action'], 'params': f_action.get('params', {})})}\n\n"

            # Catch deterministic responses (no LLM call) from respond node
            elif kind == "on_chain_end" and not full_response:
                output = event.get("data", {}).get("output", {})
                if isinstance(output, dict):
                    msgs = output.get("messages", [])
                    for msg in msgs:
                        if isinstance(msg, AIMessage) and msg.content:
                            full_response = msg.content
                            yield f"data: {json.dumps({'type': 'token', 'content': msg.content})}\n\n"

        # Store enriched conversation turn in DB
        if db is not None:
            now = datetime.now(timezone.utc).isoformat()
            turn_doc = {
                "session_id": session_id,
                "user_message": message,
                "bot_response": full_response,
                "intent": _captured_intent,
                "entities": _captured_entities,
                "tool_name": _captured_tool_name,
                "tool_result": _captured_tool_result[:2000] if _captured_tool_result else "",
                "frontend_action": _captured_frontend_action,
                "timestamp": now,
                "model": "llama-3.1-8b-instant",
                "streaming": True,
                "engine": "langgraph-rasa-v2.3",
            }
            await db.ai_chat_history.insert_one(turn_doc)

            # Save client memory if phone was identified in this session
            slot_ctx = _session_slots.get(session_id, SlotContext())
            if slot_ctx.booking.phone:
                services_discussed = []
                if slot_ctx.booking.service:
                    services_discussed.append(slot_ctx.booking.service)
                await save_conversation_memory(session_id, slot_ctx.booking.phone, {
                    "name": slot_ctx.booking.name or "",
                    "services": services_discussed,
                })

            # Update conversation session (one doc per session for analytics)
            await db.conversation_sessions.update_one(
                {"session_id": session_id},
                {
                    "$set": {
                        "last_message_at": now,
                        "last_intent": _captured_intent,
                    },
                    "$setOnInsert": {
                        "session_id": session_id,
                        "started_at": now,
                    },
                    "$inc": {"turn_count": 1},
                    "$addToSet": {
                        "intents_used": _captured_intent,
                        "tools_used": _captured_tool_name,
                    },
                },
                upsert=True,
            )

        yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"

    except Exception as e:
        print(f"[PopBot LangGraph] Error: {e}")
        import traceback
        traceback.print_exc()
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
