"""LLM-based intent classifier for PopBot — fallback when regex fails.

Only called when the regex classifier returns off_topic.
Uses Groq llama-3.1-8b-instant with temperature 0.0 for deterministic classification.
"""

import json
import os
import re
from datetime import datetime, timedelta

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from .classifier import ClassificationResult, resolve_next_weekday


VALID_INTENTS = frozenset({
    "greet", "ask_services", "ask_availability", "ask_time_slots",
    "book", "booking_continue", "cancel_booking", "lookup", "followup", "off_topic",
})

_CLASSIFIER_PROMPT = """\
Eres un clasificador de intenciones para un chatbot de salon de unas.
Hoy es {today}. El horario del salon es Lunes a Viernes, 9:00-12:00 y 16:00-19:00.

Clasifica el mensaje del usuario en UNA de estas intenciones:
- greet: saludo (hola, buenos dias, que tal, hey)
- ask_services: pregunta sobre servicios, precios, catalogo, que ofrecen
- ask_availability: pregunta sobre disponibilidad, fechas disponibles, dias libres
- ask_time_slots: pregunta sobre horarios de un dia especifico
- book: quiere agendar, reservar, hacer una cita (agendame, reservame, quiero cita, apuntame)
- booking_continue: responde a una pregunta del proceso de agenda (da nombre, telefono, email, elige servicio/fecha/hora, confirma)
- cancel_booking: quiere cancelar el proceso de agenda (olvidalo, ya no, no quiero, dejalo)
- lookup: busca su historial, da su numero de telefono
- followup: respuesta corta a pregunta anterior (si, dale, ok, cuales, muestramelos)
- off_topic: no relacionado con el salon de unas

Extrae entidades si aparecen en el mensaje:
- date: resuelve a formato YYYY-MM-DD (hoy={today}, manana={tomorrow})
- time: resuelve a formato HH:MM (ejemplo: "10 am" -> "10:00", "3 pm" -> "15:00")
- service: nombre del servicio mencionado
- phone: numero de telefono (10 digitos)

Responde UNICAMENTE con JSON valido, sin texto adicional:
{{"intent": "...", "entities": {{"date": null, "time": null, "service": null, "phone": null}}}}"""


def _get_classifier_llm():
    """Separate LLM instance for classification — temp 0.0, minimal tokens."""
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0,
        max_tokens=150,
        api_key=os.environ.get("GROQ_API_KEY"),
    )


def _parse_json_response(raw: str) -> dict | None:
    """Parse LLM response to dict with triple fallback."""
    text = raw.strip()

    # Strategy 1: direct parse
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        pass

    # Strategy 2: extract from markdown code fence
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError):
            pass

    # Strategy 3: find first {...} block
    match = re.search(r"\{[^{}]*\}", text)
    if match:
        try:
            return json.loads(match.group(0))
        except (json.JSONDecodeError, ValueError):
            pass

    return None


def _validate_date(date_str: str | None) -> str | None:
    """Validate that a date string is a real YYYY-MM-DD date."""
    if not date_str:
        return None
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return None


def _validate_time(time_str: str | None) -> str | None:
    """Validate that a time string is HH:MM format."""
    if not time_str:
        return None
    match = re.match(r"^(\d{1,2}):(\d{2})$", time_str)
    if match:
        h, m = int(match.group(1)), int(match.group(2))
        if 0 <= h <= 23 and 0 <= m <= 59:
            return f"{h:02d}:{m:02d}"
    return None


async def classify_with_llm(text: str) -> ClassificationResult:
    """Classify intent using LLM. Called only when regex returns off_topic."""
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    prompt = _CLASSIFIER_PROMPT.format(today=today, tomorrow=tomorrow)

    try:
        llm = _get_classifier_llm()
        response = await llm.ainvoke([
            SystemMessage(content=prompt),
            HumanMessage(content=text),
        ])

        parsed = _parse_json_response(response.content)
        if not parsed:
            print(f"[PopBot] LLM classifier: failed to parse JSON from: {response.content[:200]}")
            return ClassificationResult(intent="off_topic", confidence=0.0, entities={})

        # Validate intent
        intent = parsed.get("intent", "off_topic")
        if intent not in VALID_INTENTS:
            print(f"[PopBot] LLM classifier: unknown intent '{intent}', mapping to off_topic")
            intent = "off_topic"

        # Extract and validate entities
        raw_entities = parsed.get("entities", {}) or {}
        entities = {}

        date = _validate_date(raw_entities.get("date"))
        if date:
            entities["date"] = date

        time_val = _validate_time(raw_entities.get("time"))
        if time_val:
            entities["time"] = time_val

        phone = raw_entities.get("phone")
        if phone and re.match(r"^\d{10}$", str(phone)):
            entities["phone"] = str(phone)

        service = raw_entities.get("service")
        if service and isinstance(service, str) and len(service) > 1:
            entities["service"] = service

        result = ClassificationResult(
            intent=intent,
            confidence=0.85,
            entities=entities,
        )

        # Data flywheel: log every fallback
        print(
            f"[PopBot] LLM_FALLBACK: text='{text}' -> "
            f"intent={result.intent}, entities={result.entities}"
        )
        return result

    except Exception as e:
        print(f"[PopBot] LLM classifier error: {e}")
        return ClassificationResult(intent="off_topic", confidence=0.0, entities={})
