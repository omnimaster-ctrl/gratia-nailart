"""
Internal/admin utility routes for La Pop Nails.
Health check, test endpoints, reminders, migrations, and agent API.
"""

import os
import uuid
from datetime import datetime, date, timedelta, timezone
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from pymongo.errors import DuplicateKeyError
import pytz

from database import db
from auth import get_current_admin, verify_internal_token
from tenant import DEFAULT_TENANT_ID, DEFAULT_TENANT_SLUG, get_tenant_by_slug, ensure_default_tenant
from phone_utils import normalize_phone
from scheduling import is_valid_appointment_date, is_business_hours, derive_schedule, get_service_duration, get_service_price
from models import TestEmailRequest, BusinessInfo, AgentBookingRequest, BlockedDateRequest
from email_service import send_confirmation_email, send_cancellation_email
from calendar_service import create_google_calendar_event
from notification_service import create_notification
from email_service import send_owner_appointment_email
from whatsapp_service import send_whatsapp_reminder, send_whatsapp_test, send_whatsapp_confirmation

router = APIRouter(prefix="/api", tags=["internal"])


@router.get("/")
async def root():
    return {"message": "NailBookPro API - Multi-tenant nail salon booking platform"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.1.0",
        "multi_tenant": True,
        "popbot_langgraph": os.environ.get("POPBOT_USE_LANGGRAPH", "true").lower() in ("true", "1", "yes"),
    }


@router.get("/services")
async def get_services():
    """Get available services from default tenant."""
    tenant = await get_tenant_by_slug(DEFAULT_TENANT_SLUG)
    if not tenant:
        return {"services": []}

    return {
        "services": [s for s in tenant["services"] if s.get("is_active", True)]
    }


@router.get("/booking-config")
async def get_booking_config():
    """Public config for booking wizard (retiro price, anticipo, etc.)"""
    settings = await db.tenant_settings.find_one({"tenant_id": DEFAULT_TENANT_ID})
    return {
        "retiro_material_price": settings.get("retiro_material_price", 150) if settings else 150,
        "anticipo_amount": settings.get("anticipo_amount", 250) if settings else 250
    }


@router.get("/business-info")
async def get_business_info():
    """Get business information"""
    return BusinessInfo()


@router.post("/test-email")
async def test_email_endpoint(request: TestEmailRequest = TestEmailRequest(), admin=Depends(get_current_admin)):
    """Test endpoint to verify Resend email configuration works"""
    test_appointment = {
        "name": "Test Usuario",
        "date": "27 de Enero, 2026",
        "time": "10:00",
        "schedule": "Mañana (9:00 AM - 1:00 PM)",
        "service": "Uñas Acrílicas con Diseño",
        "phone": "+52 55 1234 5678",
        "notes": "Diseño floral en tonos rosa",
        "reschedule_token": "test-reschedule-token-12345"
    }

    resend_key = os.environ.get('RESEND_API_KEY', 'NOT SET')
    has_key = 'yes' if resend_key != 'NOT SET' and resend_key else 'no'

    try:
        result = await send_confirmation_email(request.email, test_appointment)
        if result:
            return {"status": "success", "message": f"Email sent successfully to {request.email} via Resend"}
        else:
            return {"status": "error", "message": f"Failed - RESEND_API_KEY set: {has_key}"}
    except Exception as e:
        return {"status": "error", "message": str(e), "resend_key_set": has_key}


@router.post("/test-cancellation-email")
async def test_cancellation_email_endpoint(request: TestEmailRequest = TestEmailRequest(), admin=Depends(get_current_admin)):
    """Test endpoint to verify cancellation email"""
    test_appointment = {
        "name": "Test Usuario",
        "date": "27 de Enero, 2026",
        "time": "10:00",
        "service": "Nivelación en uña natural",
        "reason": "Prueba del nuevo formato de email"
    }

    try:
        result = await send_cancellation_email(request.email, test_appointment)
        if result:
            return {"status": "success", "message": f"Cancellation email sent successfully to {request.email}"}
        else:
            return {"status": "error", "message": "Failed to send cancellation email"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/internal/send-reminders")
async def send_appointment_reminders(background_tasks: BackgroundTasks):
    """
    Send WhatsApp reminders for appointments scheduled for tomorrow.
    Called by Railway cron job daily at 10:00 AM Mexico City time.
    """
    try:
        mexico_tz = pytz.timezone("America/Mexico_City")
        now_mexico = datetime.now(mexico_tz)
        tomorrow = (now_mexico + timedelta(days=1)).strftime("%Y-%m-%d")

        appointments = await db.appointments.find({
            "date": tomorrow,
            "status": "confirmed",
            "reminder_sent": {"$ne": True}
        }).to_list(length=100)

        reminders_sent = 0
        for apt in appointments:
            phone = apt.get("phone", "")
            if phone:
                background_tasks.add_task(
                    send_whatsapp_reminder,
                    phone,
                    apt
                )
                await db.appointments.update_one(
                    {"id": apt["id"]},
                    {"$set": {"reminder_sent": True}}
                )
                reminders_sent += 1

        print(f"✅ Queued {reminders_sent} WhatsApp reminders for {tomorrow}")
        return {
            "status": "ok",
            "date": tomorrow,
            "reminders_queued": reminders_sent
        }

    except Exception as e:
        print(f"❌ Send reminders error: {str(e)}")
        return {"status": "error", "message": str(e)}


@router.post("/internal/test-whatsapp")
async def test_whatsapp_message(phone: str = "5214432436676", admin=Depends(get_current_admin)):
    """Send a test WhatsApp message to verify Twilio configuration."""
    try:
        success = await send_whatsapp_test(phone)
        if success:
            return {"status": "ok", "message": f"Test message sent to {phone}"}
        else:
            return {"status": "error", "message": "Failed to send - check Twilio credentials"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# =============================================================================
# AGENT API — Machine-to-machine endpoints for Clawdbot
# =============================================================================


@router.post("/internal/bookings/create")
async def agent_create_booking(
    booking: AgentBookingRequest,
    background_tasks: BackgroundTasks,
    _auth: bool = Depends(verify_internal_token),
):
    """Create a confirmed booking directly from the agent (deposit already verified)."""
    if not is_valid_appointment_date(booking.date):
        raise HTTPException(status_code=400, detail="Fecha no válida (debe ser día entre semana y con 48h de anticipación)")

    if not is_business_hours(booking.date, booking.time):
        raise HTTPException(status_code=400, detail="Horario fuera de servicio")

    existing = await db.appointments.find_one({
        "tenant_id": DEFAULT_TENANT_ID,
        "date": booking.date,
        "time": booking.time,
        "status": {"$in": ["confirmed", "pending_payment"]},
    })
    if existing:
        raise HTTPException(status_code=409, detail="Este horario ya está ocupado")

    appointment_id = str(uuid.uuid4())
    reschedule_token = str(uuid.uuid4())
    schedule = derive_schedule(booking.time)
    clean_phone = normalize_phone(booking.phone)

    appointment_doc = {
        "tenant_id": DEFAULT_TENANT_ID,
        "id": appointment_id,
        "name": booking.name,
        "phone": clean_phone,
        "service": booking.service,
        "date": booking.date,
        "time": booking.time,
        "schedule": schedule,
        "customer_email": booking.email or "",
        "status": "confirmed",
        "payment_id": "AGENT_BOOKING",
        "payment_method": "agent_direct",
        "amount_paid": 0,
        "reschedule_token": reschedule_token,
        "reschedule_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "confirmed_at": datetime.now(timezone.utc).isoformat(),
    }

    # Add client preferences if provided
    for pref_key in ["favoriteSnacks", "favoriteDrinks", "favoriteMovie", "favoriteSeries", "favoriteMusic", "birthday"]:
        val = getattr(booking, pref_key, None)
        if val:
            appointment_doc[pref_key] = val

    try:
        await db.appointments.insert_one(appointment_doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Este horario acaba de ser reservado. Por favor selecciona otro.")

    # Upsert client record (including preferences)
    client_set = {
        "phone": clean_phone,
        "name": booking.name,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if booking.email:
        client_set["email"] = booking.email
    for pref_key in ["favoriteSnacks", "favoriteDrinks", "favoriteMovie", "favoriteSeries", "favoriteMusic", "birthday"]:
        val = getattr(booking, pref_key, None)
        if val:
            client_set[pref_key] = val

    await db.clients.update_one(
        {"tenant_id": DEFAULT_TENANT_ID, "phone": clean_phone},
        {"$set": client_set, "$setOnInsert": {
            "tenant_id": DEFAULT_TENANT_ID,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }},
        upsert=True,
    )

    # Admin notification + push
    await create_notification(
        type="new_appointment",
        title="Nueva cita (agente)",
        body=f"{booking.name} - {booking.service}, {booking.date} {booking.time}",
        appointment_id=appointment_id,
    )

    # Background: WhatsApp, email, calendar, owner notification
    if clean_phone:
        background_tasks.add_task(send_whatsapp_confirmation, clean_phone, appointment_doc)
    if booking.email:
        background_tasks.add_task(send_confirmation_email, booking.email, appointment_doc)
    background_tasks.add_task(create_google_calendar_event, appointment_doc)
    background_tasks.add_task(send_owner_appointment_email, appointment_doc)

    return {
        "status": "success",
        "appointment_id": appointment_id,
        "message": "Cita confirmada",
    }


@router.get("/internal/appointments/today")
async def agent_get_today_appointments(_auth: bool = Depends(verify_internal_token)):
    """Get today's confirmed appointments (Mexico City timezone)."""
    mexico_tz = pytz.timezone("America/Mexico_City")
    today_str = datetime.now(mexico_tz).strftime("%Y-%m-%d")

    appointments = await db.appointments.find({
        "tenant_id": DEFAULT_TENANT_ID,
        "date": today_str,
        "status": {"$in": ["confirmed", "pending_payment"]},
    }).sort("time", 1).to_list(length=50)

    return {
        "date": today_str,
        "appointments": [
            {
                "id": str(apt.get("id", apt.get("_id"))),
                "name": apt.get("name"),
                "phone": apt.get("phone"),
                "service": apt.get("service"),
                "time": apt.get("time"),
                "schedule": apt.get("schedule", ""),
                "status": apt.get("status"),
                "service_duration": get_service_duration(apt.get("service")),
            }
            for apt in appointments
        ],
        "total": len(appointments),
    }


@router.get("/internal/appointments/week")
async def agent_get_week_appointments(_auth: bool = Depends(verify_internal_token)):
    """Get this week's confirmed appointments (Mon-Sat, Mexico City timezone)."""
    mexico_tz = pytz.timezone("America/Mexico_City")
    today = datetime.now(mexico_tz).date()
    monday = today - timedelta(days=today.weekday())
    saturday = monday + timedelta(days=5)

    appointments = await db.appointments.find({
        "tenant_id": DEFAULT_TENANT_ID,
        "date": {"$gte": monday.isoformat(), "$lte": saturday.isoformat()},
        "status": {"$in": ["confirmed", "pending_payment"]},
    }).sort([("date", 1), ("time", 1)]).to_list(length=100)

    return {
        "week_start": monday.isoformat(),
        "week_end": saturday.isoformat(),
        "appointments": [
            {
                "id": str(apt.get("id", apt.get("_id"))),
                "name": apt.get("name"),
                "phone": apt.get("phone"),
                "service": apt.get("service"),
                "date": apt.get("date"),
                "time": apt.get("time"),
                "schedule": apt.get("schedule", ""),
                "status": apt.get("status"),
                "service_duration": get_service_duration(apt.get("service")),
            }
            for apt in appointments
        ],
        "total": len(appointments),
    }


@router.post("/internal/blocked-dates")
async def agent_block_date(
    blocked_date: BlockedDateRequest,
    _auth: bool = Depends(verify_internal_token),
):
    """Block a date from receiving bookings (agent version)."""
    try:
        datetime.strptime(blocked_date.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    existing = await db.blocked_dates.find_one({
        "tenant_id": DEFAULT_TENANT_ID,
        "date": blocked_date.date,
    })
    if existing:
        raise HTTPException(status_code=409, detail="Esta fecha ya está bloqueada")

    blocked_doc = {
        "tenant_id": DEFAULT_TENANT_ID,
        "date": blocked_date.date,
        "reason": blocked_date.reason,
        "all_day": blocked_date.all_day,
        "created_by": "agent",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    result = await db.blocked_dates.insert_one(blocked_doc)

    return {
        "success": True,
        "message": f"Fecha bloqueada: {blocked_date.date}",
        "blocked_date": {
            "id": str(result.inserted_id),
            "date": blocked_date.date,
            "reason": blocked_date.reason,
        },
    }


# =============================================================================
# MIGRATIONS & UTILITIES
# =============================================================================


async def migrate_clients_from_appointments(rebuild: bool = False):
    """
    Backfill client records from appointments.
    Groups by phone and uses the most recent appointment per phone.
    """
    try:
        if rebuild:
            await db.clients.delete_many({"tenant_id": DEFAULT_TENANT_ID})
            print("🗑️ Cleared existing client records for rebuild")

        appointments = await db.appointments.find({
            "tenant_id": DEFAULT_TENANT_ID,
        }).sort("created_at", -1).to_list(length=10000)

        seen_phones = set()
        migrated = 0
        skipped = 0

        for apt in appointments:
            phone = apt.get("phone", "")
            if not phone:
                continue

            phone_digits = normalize_phone(phone)
            if len(phone_digits) < 10:
                continue

            if phone_digits in seen_phones:
                continue
            seen_phones.add(phone_digits)

            existing = await db.clients.find_one({
                "tenant_id": DEFAULT_TENANT_ID,
                "phone": phone_digits
            })
            if existing:
                skipped += 1
                continue

            client_doc = {
                "tenant_id": DEFAULT_TENANT_ID,
                "phone": phone_digits,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            if apt.get("name"):
                client_doc["name"] = apt.get("name")
            if apt.get("customer_email"):
                client_doc["email"] = apt.get("customer_email")
            for pref_key in ["favoriteSnacks", "favoriteDrinks", "favoriteMovie", "favoriteSeries", "favoriteMusic", "birthday"]:
                if apt.get(pref_key):
                    client_doc[pref_key] = apt.get(pref_key)

            await db.clients.insert_one(client_doc)
            migrated += 1

        print(f"✅ Client migration complete: {migrated} created, {skipped} skipped")
        return {"migrated": migrated, "skipped": skipped}

    except Exception as e:
        print(f"❌ Client migration error: {str(e)}")
        return {"error": str(e)}


@router.get("/admin/migrate-clients")
async def run_client_migration(rebuild: bool = False, admin=Depends(get_current_admin)):
    """Manually trigger client migration. Use ?rebuild=true to drop and recreate."""
    result = await migrate_clients_from_appointments(rebuild=rebuild)
    return {"status": "completed", **result}
