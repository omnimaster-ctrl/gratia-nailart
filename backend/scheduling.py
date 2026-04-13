"""
Scheduling helpers for Gratia Nail Art.
Pure business logic — date validation, availability, time slot rules.
No database access.
"""

from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

BUSINESS_TZ = ZoneInfo("America/Mexico_City")


def ensure_utc_aware(dt: datetime) -> datetime:
    """Ensure a datetime is UTC-aware. Handles naive datetimes from MongoDB."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


# Appointments with status "pending_payment" expire after this many minutes.
# Prevents failed/abandoned payments from blocking dates forever.
PENDING_PAYMENT_EXPIRY_MINUTES = 15


# ── Slot definitions (single source of truth) ──────────────────────────

WEEKDAY_MORNING_TIMES = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30"]
WEEKDAY_AFTERNOON_TIMES = ["16:00", "16:30", "17:00", "17:30", "18:00", "18:30"]
SATURDAY_MORNING_TIMES = ["10:00", "11:00"]


def derive_schedule(time_str: str) -> str:
    """Canonical schedule derivation from HH:MM. Returns 'morning' or 'afternoon'."""
    try:
        hour = int(time_str.split(":")[0])
        if 16 <= hour <= 19:
            return "afternoon"
    except (ValueError, IndexError):
        pass
    return "morning"


def get_slots_for_date(weekday: int) -> dict:
    """Return slot configuration for a weekday (0=Mon … 5=Sat).

    Keys: total_slots, has_afternoon, morning_times, afternoon_times,
          morning_label, afternoon_label, message.
    """
    if weekday == 5:  # Saturday
        return {
            "total_slots": 1,  # Una cita por día
            "has_afternoon": False,
            "morning_times": SATURDAY_MORNING_TIMES,
            "afternoon_times": [],
            "morning_label": "Mañana (10:00 AM - 11:00 AM)",
            "afternoon_label": None,
            "message": "Sábados: solo citas de 10:00 AM o 11:00 AM",
        }
    return {
        "total_slots": 1,  # Una cita por día
        "has_afternoon": True,
        "morning_times": WEEKDAY_MORNING_TIMES,
        "afternoon_times": WEEKDAY_AFTERNOON_TIMES,
        "morning_label": "Mañana (9:00 AM - 1:00 PM)",
        "afternoon_label": "Tarde (4:00 PM - 7:00 PM)",
        "message": "Selecciona el horario que prefieras",
    }


def get_valid_appointment_statuses_query():
    """
    Returns a MongoDB query that matches:
    - confirmed appointments (always valid)
    - pending_payment appointments that are less than PENDING_PAYMENT_EXPIRY_MINUTES old

    This ensures stale pending payments don't block dates forever.
    """
    cutoff_time = (datetime.now(timezone.utc) - timedelta(minutes=PENDING_PAYMENT_EXPIRY_MINUTES)).isoformat()
    return {
        "$or": [
            {"status": "confirmed"},
            {
                "status": "pending_payment",
                "created_at": {"$gte": cutoff_time}
            }
        ]
    }


def get_next_available_date():
    """Get the next available date (48 hours from now, only weekdays)"""
    now = datetime.now(BUSINESS_TZ)
    min_date = now + timedelta(hours=48)
    current_date = min_date.date()

    while current_date.weekday() > 5:
        current_date += timedelta(days=1)

    return current_date


def get_available_dates(days_ahead=30):
    """Get list of available dates for the next N days (Mon-Sat, 48h+ ahead)"""
    available_dates = []
    start_date = get_next_available_date()
    current_date = start_date
    days_added = 0

    while days_added < days_ahead:
        if current_date.weekday() <= 5:
            available_dates.append(current_date.strftime('%Y-%m-%d'))
            days_added += 1
        current_date += timedelta(days=1)

    return available_dates


def is_valid_appointment_date(date_str: str) -> bool:
    """Check if the appointment date is valid (48h+ ahead, Mon-Sat)"""
    try:
        appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        min_date = get_next_available_date()

        if appointment_date < min_date:
            return False

        if appointment_date.weekday() > 5:
            return False

        return True
    except ValueError:
        return False


def is_business_hours(date_str: str, time_str: str) -> bool:
    """Check if appointment is within business hours"""
    try:
        appointment_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        weekday = appointment_datetime.weekday()

        if weekday > 5:
            return False

        appointment_time = appointment_datetime.time()

        # Saturday has special hours: 10:00-12:00 only
        if weekday == 5:
            saturday_start = time(10, 0)
            saturday_end = time(12, 0)
            return saturday_start <= appointment_time <= saturday_end

        # Monday-Friday hours
        morning_start = time(9, 0)
        morning_end = time(13, 0)
        afternoon_start = time(16, 0)
        afternoon_end = time(19, 0)

        return (morning_start <= appointment_time <= morning_end) or \
               (afternoon_start <= appointment_time <= afternoon_end)
    except ValueError:
        return False


def get_service_duration(service_name: str) -> str:
    """Get service duration as formatted string."""
    service_durations = {
        "Técnica Mixta": "3h",
        "Nail Art Completo": "4h",
        "Retoque / Mantenimiento": "2h"
    }
    return service_durations.get(service_name, "Variable")


def get_service_price(service_name: str) -> float:
    """Get service price."""
    service_prices = {
        "Técnica Mixta": 500.00,
        "Nail Art Completo": 700.00,
        "Retoque / Mantenimiento": 400.00
    }
    return service_prices.get(service_name, 0.00)


def generate_instagram_message(appointment: dict) -> str:
    """Generate Instagram message for appointment confirmation"""
    return f"""¡Hola {appointment['name']}! Tu cita en Gratia Nail Art ha sido confirmada ✨

📅 Fecha: {appointment['date']}
🕐 Hora: {appointment['time']}
💅 Servicio: {appointment['service']}
📱 Teléfono: {appointment['phone']}

{f"📝 Notas: {appointment['notes']}" if appointment.get('notes') else ""}

💰 Anticipo pagado: $250 MXN
✅ Estado: Confirmada

¡Te esperamos para crear arte en tus uñas! 🧚‍♂️✨

- Gratia Nail Art"""
