"""
Appointment query and availability routes for La Pop Nails.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from database import db
from tenant import DEFAULT_TENANT_ID
from scheduling import (
    derive_schedule,
    ensure_utc_aware,
    get_available_dates,
    get_next_available_date,
    get_slots_for_date,
    get_valid_appointment_statuses_query,
    is_valid_appointment_date,
)

router = APIRouter(prefix="/api", tags=["appointments"])


@router.get("/appointment/{appointment_id}")
async def get_appointment_status(appointment_id: str):
    """Get appointment status"""
    try:
        appointment = await db.appointments.find_one({"id": appointment_id})

        if not appointment:
            raise HTTPException(status_code=404, detail="Cita no encontrada")

        return {
            "appointment_id": appointment["id"],
            "status": appointment["status"],
            "name": appointment["name"],
            "service": appointment["service"],
            "date": appointment["date"],
            "time": appointment["time"],
            "payment_status": appointment.get("payment_status"),
            "confirmed_at": appointment.get("confirmed_at")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la cita: {str(e)}")


@router.get("/appointments")
async def get_appointments():
    """Get all appointments for default tenant (legacy endpoint)"""
    try:
        appointments = await db.appointments.find({"tenant_id": DEFAULT_TENANT_ID}).to_list(length=100)
        for apt in appointments:
            apt.pop("_id", None)
        return {"appointments": appointments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving appointments: {str(e)}")


@router.get("/available-dates")
async def get_available_appointment_dates():
    """Get available dates for default tenant (legacy endpoint)"""
    try:
        available_dates = get_available_dates(30)

        tenant_settings = await db.tenant_settings.find_one({
            "tenant_id": DEFAULT_TENANT_ID
        })
        one_appointment_per_day = tenant_settings.get("one_appointment_per_day", False) if tenant_settings else False

        status_query = get_valid_appointment_statuses_query()
        confirmed_appointments = await db.appointments.find({
            "tenant_id": DEFAULT_TENANT_ID,
            **status_query
        }).to_list(length=1000)

        appointments_by_date = {}
        for apt in confirmed_appointments:
            date = apt["date"]
            if date not in appointments_by_date:
                appointments_by_date[date] = []
            appointments_by_date[date].append(apt["time"])

        blocked_dates_docs = await db.blocked_dates.find({
            "tenant_id": DEFAULT_TENANT_ID
        }).to_list(length=1000)
        blocked_dates_set = {bd.get("date") for bd in blocked_dates_docs if bd.get("date")}

        dates_with_availability = []
        for date in available_dates:
            if date in blocked_dates_set:
                continue

            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            if date_obj.weekday() > 5:
                continue

            if one_appointment_per_day:
                if date in appointments_by_date and len(appointments_by_date[date]) > 0:
                    dates_with_availability.append({
                        "date": date,
                        "available_slots": 0,
                        "is_available": False
                    })
                    continue
                else:
                    dates_with_availability.append({
                        "date": date,
                        "available_slots": 1,
                        "is_available": True
                    })
                    continue

            slots_config = get_slots_for_date(date_obj.weekday())

            booked_count = len(appointments_by_date.get(date, []))
            available_slots = slots_config["total_slots"] - booked_count

            dates_with_availability.append({
                "date": date,
                "available_slots": available_slots,
                "is_available": available_slots > 0
            })

        return {
            "available_dates": dates_with_availability,
            "min_date": get_next_available_date().strftime('%Y-%m-%d')
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener fechas disponibles: {str(e)}")


@router.get("/available-times/{date}")
async def get_available_times(date: str):
    """Get available appointment times for a specific date"""
    try:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

        if not is_valid_appointment_date(date):
            raise HTTPException(
                status_code=400,
                detail="La fecha debe ser al menos 48 horas después de ahora y en día laboral (Lunes-Sábado)"
            )

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        slots_config = get_slots_for_date(date_obj.weekday())

        status_query = get_valid_appointment_statuses_query()
        existing_appointments = await db.appointments.find({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": date,
            **status_query
        }).to_list(length=100)

        booked_times = []
        morning_booking = None

        for apt in existing_appointments:
            apt_time = apt.get("time", "")
            apt_service = apt.get("service", "")
            if apt_time:
                booked_times.append(apt_time)
                if derive_schedule(apt_time) == "morning":
                    morning_booking = {"time": apt_time, "service": apt_service}

        booked_times_set = set(booked_times)

        # Build available times by filtering out individually booked slots
        available_schedules = []
        available_times = []

        morning_available = [t for t in slots_config["morning_times"] if t not in booked_times_set]
        if morning_available:
            available_schedules.append(slots_config["morning_label"])
            available_times.extend(morning_available)

        if slots_config["has_afternoon"]:
            afternoon_available = [t for t in slots_config["afternoon_times"] if t not in booked_times_set]
            if afternoon_available:
                available_schedules.append(slots_config["afternoon_label"])
                available_times.extend(afternoon_available)

        # Check for active holds on this date (per-schedule)
        now = datetime.now(timezone.utc)
        active_holds = await db.booking_holds.find({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": date,
            "expires_at": {"$gt": now},
        }).to_list(length=10)

        holds = {}
        for hold in active_holds:
            schedule = hold.get("schedule", "morning")
            remaining = (ensure_utc_aware(hold["expires_at"]) - now).total_seconds() / 60
            holds[schedule] = {
                "active": True,
                "expires_at": ensure_utc_aware(hold["expires_at"]).isoformat(),
                "remaining_minutes": round(remaining, 1),
            }

        return {
            "available_times": available_times,
            "available_schedules": available_schedules,
            "booked_schedules": [],  # Deprecated: no more block-level blocking
            "booked_times": booked_times,
            "morning_booking": morning_booking,
            "total_slots": slots_config["total_slots"],
            "message": slots_config["message"],
            "holds": holds if holds else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener horarios: {str(e)}")
