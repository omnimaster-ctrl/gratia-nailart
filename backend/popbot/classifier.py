"""Rasa-inspired intent classifier and slot context for PopBot."""

import re
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timedelta


@dataclass
class ClassificationResult:
    intent: str
    confidence: float
    entities: dict = field(default_factory=dict)


@dataclass
class BookingSlots:
    """Accumulated booking fields across conversation turns."""
    active: bool = False
    phone: str = ""
    name: str = ""
    email: str = ""
    service: str = ""        # Exact service name from catalog
    date: str = ""           # YYYY-MM-DD
    time: str = ""           # HH:MM
    schedule: str = ""       # Derived: "Mañana" or "Tarde"
    awaiting_field: str = "" # What we last asked for
    client_found: bool = False
    date_rejection: str = "" # Why a date was rejected (48h, Sunday, etc.)
    time_rejection: str = "" # Why a time was rejected (outside hours, etc.)


@dataclass
class SlotContext:
    """Stores the last tool result for followup resolution."""
    last_intent: str = ""
    last_tool_result: str = ""
    last_tool_name: str = ""
    booking: BookingSlots = field(default_factory=BookingSlots)


# Intent patterns ordered by specificity (most specific first)
INTENT_PATTERNS = [
    ("greet", [
        r"\b(hola|buenos?\s*d[ií]as?|buenas?\s*(tardes?|noches?)|que\s*tal|hey|hi)\b",
    ]),
    ("ask_services", [
        r"\b(servicios?|precios?|cu[aá]nto\s*cuesta|qu[eé]\s*ofrecen|men[uú]|cat[aá]logo)\b",
        r"\b(manicur[ao]|u[nñ]as?|nivelaci[oó]n|extensi[oó]n|refuerzo|h[ií]brid[ao]|rusa|escultural)\b",
    ]),
    ("ask_availability", [
        r"\b(disponibilidad|disponibles?)\b",
        r"\b(fechas?\s*(disponibles?)?|d[ií]as?\s*(libres?|disponibles?)?)\b",
        r"\b(cu[aá]ndo\s*hay|hay\s*(lugar|espacio|disponibilidad|fechas?|horarios?)|hay\s*citas?)\b",
        r"\b(pr[oó]xim[ao]s?\s*(fechas?|d[ií]as?))\b",
        r"\b(checar|ver|revisar)\s+(horarios?|citas?|fechas?)\b",
        r"\bhorarios?\b",
    ]),
    ("ask_time_slots", [
        r"\b(qu[eé]\s*horas?|a\s*qu[eé]\s*hora)\b",
        r"\bhorarios?\b.*\b(lunes|martes|mi[eé]rcoles|jueves|viernes)\b",
        r"\b(lunes|martes|mi[eé]rcoles|jueves|viernes)\b.*\bhorarios?\b",
    ]),
    ("book", [
        r"\b(agendar|reservar|quiero\s*cita|quiero\s*agendar)\b",
        r"\b(ag[eé]ndame|res[eé]rvame|ap[uú]ntame|ag[eé]ndalo|res[eé]rvalo)\b",
        r"\b(quiero|necesito|quisiera|me\s*gustar[ií]a|ocupo)\s*(una\s*)?(cita|reserva|reservaci[oó]n)\b",
        r"\b(me\s*agendas?|me\s*reservas?|me\s*apartas?)\b",
        r"^(s[ií]\s*quiero|dale\s*agenda|ok\s*reserva|va\s*que\s*va)\s*[.!?]*$",
    ]),
    ("cancel_booking", [
        r"\b(no\s*quiero|olv[ií]da(lo)?|d[eé]jalo|ya\s*no|no\s*gracias)\b",
    ]),
    ("lookup", [
        r"\b(mi\s*tel[eé]fono|buscar\s*(mi|el)?\s*(historial|registro)|mi\s*n[uú]mero)\b",
        r"\b\d{10}\b",
    ]),
    ("followup", [
        r"^(d[aá]melas?|cu[aá]les|mu[eé]stral[ao]s?|dime|enl[ií]stal[ao]s?)\s*[.!?]*$",
        r"^(s[ií]|ok|dale|listo|va)\s*[.!?]*$",
    ]),
]

PHONE_PATTERN = re.compile(r"(\d{10})")
DATE_PATTERN = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
EMAIL_PATTERN = re.compile(r"[\w.-]+@[\w.-]+\.\w{2,}")
DAY_NAMES = {
    "lunes": 0, "martes": 1, "miercoles": 2, "miércoles": 2,
    "jueves": 3, "viernes": 4,
}

# Natural time patterns
TIME_PATTERN = re.compile(
    r"(?:a\s*las?\s*)?(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?",
    re.IGNORECASE,
)

MONTH_NAMES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}


def _extract_natural_date(text: str) -> str | None:
    """Extract date from natural language: manana, pasado manana, 3 de febrero."""
    now = datetime.now()

    if re.search(r"\bpasado\s*ma[nñ]ana\b", text):
        return (now + timedelta(days=2)).strftime("%Y-%m-%d")
    if re.search(r"\bma[nñ]ana\b", text):
        # Avoid matching "en la manana" (time hint, not date)
        if not re.search(r"\b(de\s*la|en\s*la|por\s*la)\s*ma[nñ]ana\b", text):
            return (now + timedelta(days=1)).strftime("%Y-%m-%d")
    if re.search(r"\bhoy\b", text):
        return now.strftime("%Y-%m-%d")

    # "3 de febrero", "15 de marzo"
    match = re.search(r"\b(\d{1,2})\s+de\s+(\w+)\b", text)
    if match:
        day = int(match.group(1))
        month_name = match.group(2).lower()
        if month_name in MONTH_NAMES:
            month = MONTH_NAMES[month_name]
            year = now.year
            try:
                dt = datetime(year, month, day)
                if dt.date() < now.date():
                    year += 1
                return f"{year}-{month:02d}-{day:02d}"
            except ValueError:
                pass

    return None


def _extract_natural_time(text: str) -> str | None:
    """Extract time from natural language: 10 am, a las 3, 10:30."""
    # "en la manana" / "por la tarde" → time hint
    if re.search(r"\b(de|en|por)\s*la\s*ma[nñ]ana\b", text):
        return "morning"
    if re.search(r"\b(de|en|por)\s*la\s*tarde\b", text):
        return "afternoon"

    match = TIME_PATTERN.search(text)
    if match:
        hour = int(match.group(1))
        minutes = match.group(2) or "00"
        period = (match.group(3) or "").replace(".", "").lower()

        if period == "pm" and hour < 12:
            hour += 12
        elif period == "am" and hour == 12:
            hour = 0
        elif not period and hour < 8:
            # Bare small numbers likely PM for a salon (e.g., "a las 4" → 16:00)
            hour += 12

        if 0 <= hour <= 23:
            return f"{hour:02d}:{minutes}"

    return None


def classify(text: str, slot_ctx: Optional[SlotContext] = None) -> ClassificationResult:
    """Classify user intent using regex patterns."""
    normalized = text.lower().strip()
    clean = re.sub(r'[¿¡!?,.]', '', normalized)

    entities = {}

    phone_match = PHONE_PATTERN.search(normalized)
    if phone_match:
        entities["phone"] = phone_match.group(1)

    email_match = EMAIL_PATTERN.search(normalized)
    if email_match:
        entities["email"] = email_match.group(0)

    date_match = DATE_PATTERN.search(normalized)
    if date_match:
        entities["date"] = date_match.group(1)

    for day_name, weekday_num in DAY_NAMES.items():
        if day_name in clean:
            entities["day_name"] = day_name
            entities["weekday"] = weekday_num
            break

    # Natural date extraction: "manana", "pasado manana", "3 de febrero"
    if "date" not in entities:
        natural_date = _extract_natural_date(clean)
        if natural_date:
            entities["date"] = natural_date

    # Natural time extraction: "10 am", "a las 3", "en la tarde"
    natural_time = _extract_natural_time(clean)
    if natural_time:
        entities["time"] = natural_time

    # Match intents (first match wins due to specificity ordering)
    for intent_name, patterns in INTENT_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, clean):
                result = ClassificationResult(
                    intent=intent_name,
                    confidence=0.9,
                    entities=entities,
                )
                # Resolve ambiguous followup vs book
                result = _resolve_ambiguity(result, clean, slot_ctx)
                return result

    # No regex match — still apply ambiguity resolution (e.g. booking-active override)
    result = ClassificationResult(intent="off_topic", confidence=0.5, entities=entities)
    result = _resolve_ambiguity(result, clean, slot_ctx)
    return result


def _resolve_ambiguity(
    result: ClassificationResult,
    clean_text: str,
    slot_ctx: Optional[SlotContext],
) -> ClassificationResult:
    """Resolve ambiguous classifications using slot context."""
    ctx = slot_ctx or SlotContext()

    # Active booking: most intents become booking_continue
    if ctx.booking.active:
        # Cancel overrides everything
        if result.intent == "cancel_booking":
            return result
        # Info questions mid-booking: let them through (user can ask prices etc.)
        if result.intent in ("ask_services", "ask_availability", "ask_time_slots"):
            return result
        # Everything else during active booking = booking_continue
        if result.intent in ("followup", "off_topic", "greet", "book", "lookup"):
            result.intent = "booking_continue"
            return result

    # Cancel when no booking active: treat as off_topic
    if result.intent == "cancel_booking" and not ctx.booking.active:
        result.intent = "off_topic"

    # Bare "si", "dale", "listo" after an info question = followup, not booking
    if result.intent == "followup":
        bare_confirm = clean_text in ("si", "sí", "ok", "dale", "listo", "va")
        if bare_confirm and ctx.last_intent in ("ask_availability", "ask_time_slots", "ask_services"):
            result.intent = "followup"
        elif bare_confirm and ctx.last_intent == "book":
            result.intent = "book"
        elif bare_confirm and not ctx.last_intent:
            # No prior context, treat as greeting
            result.intent = "greet"

    # If followup but no cached data and no prior intent, downgrade
    if result.intent == "followup" and not ctx.last_tool_result and not ctx.last_intent:
        result.intent = "greet"

    return result


def resolve_next_weekday(target_weekday: int) -> str:
    """Resolve day name to next YYYY-MM-DD occurrence (48h+ ahead)."""
    now = datetime.now()
    min_date = (now + timedelta(hours=48)).date()
    current = min_date
    for _ in range(7):
        if current.weekday() == target_weekday:
            return current.strftime("%Y-%m-%d")
        current += timedelta(days=1)
    return min_date.strftime("%Y-%m-%d")
