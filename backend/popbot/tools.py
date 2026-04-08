"""Data-fetching functions for PopBot (plain async, no LangChain tool decorators)."""

import re
from datetime import datetime, timedelta, timezone
from typing import Optional
from phone_utils import normalize_phone
from scheduling import BUSINESS_TZ, derive_schedule as _derive_schedule_key


_db = None
_tenant_id = None


def init_tools(db, tenant_id: str):
    """Initialize tools with database connection and tenant context."""
    global _db, _tenant_id
    _db = db
    _tenant_id = tenant_id


def _get_valid_appointment_statuses_query():
    """Returns MongoDB query matching valid (non-expired) appointments."""
    cutoff_time = (datetime.now(timezone.utc) - timedelta(minutes=15)).isoformat()
    return {
        "$or": [
            {"status": "confirmed"},
            {
                "status": "pending_payment",
                "created_at": {"$gte": cutoff_time},
            },
        ]
    }


def _get_next_available_date():
    """Get the next available date (48 hours from now, Mon-Sat)."""
    now = datetime.now(BUSINESS_TZ)
    min_date = now + timedelta(hours=48)
    current_date = min_date.date()
    while current_date.weekday() > 5:  # Skip Sunday only
        current_date += timedelta(days=1)
    return current_date


def _get_available_dates_list(days_ahead=30):
    """Get list of available dates (Mon-Sat) starting from 48h ahead."""
    available_dates = []
    current_date = _get_next_available_date()
    days_added = 0
    while days_added < days_ahead:
        if current_date.weekday() <= 5:  # Mon-Sat
            available_dates.append(current_date.strftime("%Y-%m-%d"))
            days_added += 1
        current_date += timedelta(days=1)
    return available_dates


async def get_services_data() -> str:
    """Fetch services list with prices."""
    if _db is None:
        return "No hay servicios disponibles."

    tenant = await _db.tenants.find_one({"slug": "lapopnails", "status": "active"})
    if not tenant:
        return "No hay servicios disponibles."

    services = [s for s in tenant.get("services", []) if s.get("is_active", True)]
    if not services:
        return "No hay servicios disponibles."

    result = "Servicios disponibles:\n"
    for s in services:
        name = s.get("name", "Servicio")
        price = s.get("price", s.get("base_price", "?"))
        result += f"- {name}: ${price} MXN"
        if s.get("duration_range"):
            result += f" ({s['duration_range']})"
        result += "\n"
    return result.strip()


async def get_available_dates_data() -> str:
    """Fetch next available dates."""
    if _db is None:
        return "No pude verificar disponibilidad."

    try:
        dates_list = _get_available_dates_list(30)

        status_query = _get_valid_appointment_statuses_query()
        confirmed = await _db.appointments.find(
            {"tenant_id": _tenant_id, **status_query}
        ).to_list(length=1000)

        by_date = {}
        for apt in confirmed:
            d = apt["date"]
            by_date[d] = by_date.get(d, 0) + 1

        available = []
        for d in dates_list[:15]:
            if by_date.get(d, 0) < 2:
                available.append(d)
            if len(available) >= 5:
                break

        if not available:
            return "No hay fechas disponibles en los proximos dias. Por favor intenta mas adelante."

        day_names = [
            "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo",
        ]
        month_names = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        ]

        formatted = []
        for d in available:
            dt = datetime.strptime(d, "%Y-%m-%d")
            formatted.append(f"{day_names[dt.weekday()]} {dt.day} de {month_names[dt.month - 1]}")

        return f"Fechas disponibles: {', '.join(formatted)}. Puedes agendar usando el boton Agendar Cita."

    except Exception as e:
        print(f"Error in get_available_dates_data: {e}")
        return "No pude verificar disponibilidad. Usa el boton Agendar Cita para ver fechas."


async def get_time_slots_data(date: str) -> str:
    """Fetch available time slots for a specific date."""
    if _db is None:
        return "No pude obtener horarios."

    try:
        datetime.strptime(date, "%Y-%m-%d")

        status_query = _get_valid_appointment_statuses_query()
        existing = await _db.appointments.find(
            {"tenant_id": _tenant_id, "date": date, **status_query}
        ).to_list(length=100)

        booked_times = [apt.get("time") for apt in existing]

        morning = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00"]
        afternoon = ["16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00"]

        avail_morning = [t for t in morning if t not in booked_times]
        avail_afternoon = [t for t in afternoon if t not in booked_times]

        if not avail_morning and not avail_afternoon:
            return f"No hay horarios disponibles para {date}."

        result = f"Horarios para {date}:\n"
        if avail_morning:
            result += f"Manana: {', '.join(avail_morning)}\n"
        if avail_afternoon:
            result += f"Tarde: {', '.join(avail_afternoon)}"

        return result.strip()

    except ValueError:
        return "Fecha invalida. Usa formato YYYY-MM-DD."
    except Exception as e:
        print(f"Error in get_time_slots_data: {e}")
        return "No pude obtener horarios."


async def lookup_client_data(phone: str) -> str:
    """Look up client by phone number."""
    if _db is None:
        return "No pude buscar el cliente."

    try:
        clean_phone = normalize_phone(phone)

        client = await _db.clients.find_one(
            {"tenant_id": _tenant_id, "phone": clean_phone}
        )

        if not client:
            return "No encontre registros con ese numero. Es tu primera visita? Bienvenida!"

        name = client.get("name", "")
        count = client.get("appointment_count", 0)

        response = f"Hola {name}! Que gusto verte de nuevo."
        if count > 0:
            response += f" Ya tienes {count} citas con nosotros."

        return response

    except Exception as e:
        print(f"Error in lookup_client_data: {e}")
        return "No pude buscar el cliente."


async def start_booking_action(service: Optional[str] = None) -> str:
    """Trigger booking flow. Returns text for the user."""
    return "Voy a abrir el formulario de reserva para que puedas agendar tu cita."


# ── Booking Slot-Filling Helpers ──────────────────────────────────

SERVICE_CATALOG = {
    "1": "Nivelación en uña natural",
    "2": "Refuerzo con técnica híbrida",
    "3": "Extensión híbrida",
    "nivelacion": "Nivelación en uña natural",
    "nivelación": "Nivelación en uña natural",
    "natural": "Nivelación en uña natural",
    "refuerzo": "Refuerzo con técnica híbrida",
    "hibrida": "Refuerzo con técnica híbrida",
    "híbrida": "Refuerzo con técnica híbrida",
    "extension": "Extensión híbrida",
    "extensión": "Extensión híbrida",
    "escultural": "Extensión híbrida",
}

SERVICE_PRICES = {
    "Nivelación en uña natural": 500,
    "Refuerzo con técnica híbrida": 600,
    "Extensión híbrida": 700,
}

DAY_NAMES_ES = [
    "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo",
]
MONTH_NAMES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def match_service(text: str) -> str | None:
    """Match user text to exact service name from catalog."""
    clean = text.lower().strip()
    # Direct key match
    if clean in SERVICE_CATALOG:
        return SERVICE_CATALOG[clean]
    # Substring match
    for key, service_name in SERVICE_CATALOG.items():
        if key in clean:
            return service_name
    return None


def derive_schedule(time_str: str) -> str:
    """Map HH:MM to schedule display label for PopBot (delegates to canonical derive_schedule)."""
    key = _derive_schedule_key(time_str)
    if key == "afternoon":
        return "Tarde (4:00 PM - 7:00 PM)"
    return "Mañana (9:00 AM - 1:00 PM)"


def format_date_es(date_str: str) -> str:
    """Format YYYY-MM-DD as 'Martes 4 de febrero'."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{DAY_NAMES_ES[dt.weekday()]} {dt.day} de {MONTH_NAMES_ES[dt.month - 1]}"
    except ValueError:
        return date_str


async def get_available_dates_for_booking() -> list[str]:
    """Get formatted available dates for booking slot-filling."""
    if _db is None:
        return []

    try:
        dates_list = _get_available_dates_list(30)
        status_query = _get_valid_appointment_statuses_query()
        confirmed = await _db.appointments.find(
            {"tenant_id": _tenant_id, **status_query}
        ).to_list(length=1000)

        by_date = {}
        for apt in confirmed:
            d = apt["date"]
            by_date[d] = by_date.get(d, 0) + 1

        available = []
        for d in dates_list[:15]:
            if by_date.get(d, 0) < 2:
                available.append(d)
            if len(available) >= 5:
                break
        return available
    except Exception as e:
        print(f"Error in get_available_dates_for_booking: {e}")
        return []


async def get_time_slots_for_booking(date: str) -> dict:
    """Get structured time slots for booking slot-filling."""
    if _db is None:
        return {"morning": [], "afternoon": []}

    try:
        status_query = _get_valid_appointment_statuses_query()
        existing = await _db.appointments.find(
            {"tenant_id": _tenant_id, "date": date, **status_query}
        ).to_list(length=100)

        booked_times = [apt.get("time") for apt in existing]

        morning = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00"]
        afternoon = ["16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00"]

        return {
            "morning": [t for t in morning if t not in booked_times],
            "afternoon": [t for t in afternoon if t not in booked_times],
        }
    except Exception as e:
        print(f"Error in get_time_slots_for_booking: {e}")
        return {"morning": [], "afternoon": []}


async def lookup_client_record(phone: str) -> dict | None:
    """Look up client record by phone. Returns full dict or None."""
    if _db is None:
        return None
    try:
        clean_phone = normalize_phone(phone)
        return await _db.clients.find_one(
            {"tenant_id": _tenant_id, "phone": clean_phone}
        )
    except Exception:
        return None


async def get_client_memory(phone: str) -> dict | None:
    """Fetch client memory for a returning client. Returns context for personalization."""
    if _db is None or not phone:
        return None
    try:
        clean_phone = normalize_phone(phone)
        client = await _db.clients.find_one(
            {"tenant_id": _tenant_id, "phone": clean_phone}
        )
        if not client:
            return None

        # Get last 3 confirmed appointments for this client
        appointments = await _db.appointments.find(
            {"tenant_id": _tenant_id, "phone": clean_phone, "status": "confirmed"}
        ).sort("date", -1).to_list(length=3)

        memory = {
            "name": client.get("name", ""),
            "appointment_count": client.get("appointment_count", 0),
            "last_service": None,
            "preferred_schedule": None,
            "history": [],
        }

        if appointments:
            last = appointments[0]
            memory["last_service"] = last.get("service", "")
            memory["last_date"] = last.get("date", "")

            # Detect schedule preference from history
            schedules = []
            for apt in appointments:
                t = apt.get("time", "")
                if t:
                    hour = int(t.split(":")[0])
                    schedules.append("morning" if hour < 13 else "afternoon")
                memory["history"].append({
                    "service": apt.get("service", ""),
                    "date": apt.get("date", ""),
                })

            if schedules:
                from collections import Counter
                most_common = Counter(schedules).most_common(1)[0][0]
                memory["preferred_schedule"] = "mañana" if most_common == "morning" else "tarde"

        return memory
    except Exception as e:
        print(f"Error in get_client_memory: {e}")
        return None


async def save_conversation_memory(session_id: str, phone: str, summary: dict):
    """Save conversation-level memory after a session with a known client."""
    if _db is None or not phone:
        return
    try:
        clean_phone = normalize_phone(phone)
        await _db.client_memories.update_one(
            {"tenant_id": _tenant_id, "phone": clean_phone},
            {
                "$set": {
                    "phone": clean_phone,
                    "tenant_id": _tenant_id,
                    "last_session_id": session_id,
                    "last_interaction": datetime.now(timezone.utc).isoformat(),
                    "name": summary.get("name", ""),
                },
                "$addToSet": {
                    "services_discussed": {"$each": summary.get("services", [])},
                },
                "$inc": {"total_conversations": 1},
            },
            upsert=True,
        )
    except Exception as e:
        print(f"Error saving conversation memory: {e}")


def validate_booking_date(date_str: str) -> dict:
    """Validate a booking date. Returns {valid: bool, error: str}."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return {"valid": False, "error": "Fecha invalida."}

    now = datetime.now(BUSINESS_TZ)
    min_date = (now + timedelta(hours=48)).date()

    if dt.date() < min_date:
        return {"valid": False, "error": f"La cita debe ser con al menos 48 horas de anticipacion. La fecha mas proxima es {min_date.strftime('%Y-%m-%d')}."}

    if dt.weekday() > 5:  # Sunday
        return {"valid": False, "error": "No trabajamos los domingos. Elige un dia de lunes a sabado."}

    return {"valid": True, "error": ""}


def validate_booking_time(time_str: str, date_str: str = "") -> dict:
    """Validate a booking time is within business hours."""
    try:
        parts = time_str.split(":")
        hour, minute = int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        return {"valid": False, "error": "Hora invalida."}

    # Check if Saturday
    is_saturday = False
    if date_str:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            is_saturday = dt.weekday() == 5
        except ValueError:
            pass

    if is_saturday:
        if 10 <= hour < 12:
            return {"valid": True, "error": ""}
        return {"valid": False, "error": "Los sabados atendemos de 10:00 AM a 12:00 PM."}

    # Weekday hours
    morning = 9 <= hour < 13
    afternoon = 16 <= hour <= 19
    if morning or afternoon:
        return {"valid": True, "error": ""}

    return {"valid": False, "error": "Nuestro horario es 9:00-13:00 y 16:00-19:00 de lunes a viernes."}
