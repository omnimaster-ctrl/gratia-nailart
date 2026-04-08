"""
Reschedule routes for La Pop Nails.
Legacy email/phone verification and token-based self-service reschedule.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
import pytz

from database import db
from tenant import DEFAULT_TENANT_ID
from scheduling import is_valid_appointment_date, is_business_hours
from models import RescheduleRequest, RescheduleUpdate, TokenRescheduleRequest
from email_service import send_confirmation_email, send_reschedule_blocked_notification
from calendar_service import create_google_calendar_event
from whatsapp_service import send_whatsapp_confirmation

router = APIRouter(prefix="/api", tags=["reschedule"])


@router.post("/reschedule/verify")
async def verify_reschedule_eligibility(request: RescheduleRequest):
    """Verify if user can reschedule their appointment (legacy endpoint for default tenant)"""
    try:
        appointments = await db.appointments.find({
            "tenant_id": DEFAULT_TENANT_ID,
            "customer_email": request.email,
            "phone": request.phone,
            "status": "confirmed"
        }).to_list(length=10)

        if not appointments:
            raise HTTPException(
                status_code=404,
                detail="No se encontró ninguna cita confirmada con estos datos. Verifica tu email y teléfono."
            )

        latest_appointment = max(appointments, key=lambda x: x.get('confirmed_at', ''))

        reschedule_count = latest_appointment.get('reschedule_count', 0)

        if reschedule_count >= 1:
            try:
                await send_reschedule_blocked_notification(
                    request.email,
                    latest_appointment["name"],
                    latest_appointment["date"],
                    latest_appointment["schedule"]
                )
                print(f"📧 Sent reschedule blocked notification to {request.email}")
            except Exception as email_error:
                print(f"⚠️ Failed to send reschedule blocked email: {email_error}")

            raise HTTPException(
                status_code=403,
                detail="Ya reagendaste esta cita anteriormente. Solo se permite reagendar una vez por cita confirmada.\n\n✨ ¿Necesitas cambiar tu fecha nuevamente?\n🆕 Puedes agendar una NUEVA CITA con un nuevo anticipo de $250 MXN.\n📞 O contáctanos por Instagram @___lapopnails para más opciones.\n\n¡Te esperamos para crear magia en tus uñas! 💅"
            )

        return {
            "appointment_id": latest_appointment["id"],
            "current_date": latest_appointment["date"],
            "current_time": latest_appointment["time"],
            "current_schedule": latest_appointment["schedule"],
            "service": latest_appointment["service"],
            "reschedule_count": reschedule_count,
            "can_reschedule": True,
            "message": "¡Puedes reagendar tu cita! Selecciona una nueva fecha y horario."
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar elegibilidad: {str(e)}")


@router.post("/reschedule/update")
async def update_appointment_schedule(request: RescheduleUpdate):
    """Update appointment schedule for eligible users"""
    try:
        if not is_valid_appointment_date(request.new_date):
            raise HTTPException(
                status_code=400,
                detail="La nueva fecha debe ser al menos 48 horas después de ahora y en día laboral (Lunes-Viernes)"
            )

        if not is_business_hours(request.new_date, request.new_time):
            raise HTTPException(
                status_code=400,
                detail="La nueva cita debe ser de Lunes a Viernes, entre 9:00-12:00 AM o 4:00-7:00 PM"
            )

        existing = await db.appointments.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": request.new_date,
            "time": request.new_time,
            "status": "confirmed"
        })

        if existing:
            raise HTTPException(
                status_code=400,
                detail="El nuevo horario ya está ocupado. Por favor selecciona otro."
            )

        current_appointment = await db.appointments.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "customer_email": request.email,
            "phone": request.phone,
            "status": "confirmed"
        })

        if not current_appointment:
            raise HTTPException(
                status_code=404,
                detail="No se encontró tu cita actual para reagendar."
            )

        reschedule_count = current_appointment.get('reschedule_count', 0)
        if reschedule_count >= 1:
            raise HTTPException(
                status_code=403,
                detail="Ya has reagendado esta cita anteriormente. Solo se permite reagendar una vez."
            )

        update_result = await db.appointments.update_one(
            {"_id": current_appointment["_id"]},
            {
                "$set": {
                    "date": request.new_date,
                    "schedule": request.new_schedule,
                    "time": request.new_time,
                    "reschedule_count": reschedule_count + 1,
                    "rescheduled_at": datetime.now(timezone.utc).isoformat(),
                    "previous_date": current_appointment["date"],
                    "previous_time": current_appointment["time"],
                    "previous_schedule": current_appointment["schedule"]
                }
            }
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar la cita. Inténtalo nuevamente."
            )

        updated_appointment = await db.appointments.find_one({"_id": current_appointment["_id"]})

        if updated_appointment:
            try:
                await send_confirmation_email(
                    updated_appointment["customer_email"],
                    updated_appointment
                )
                await create_google_calendar_event(updated_appointment)
                print(f"✅ Reschedule successful for {request.email}")
            except Exception as notification_error:
                print(f"⚠️ Reschedule successful but notification failed: {notification_error}")

        return {
            "success": True,
            "message": "¡Cita reagendada exitosamente! Recibirás un email de confirmación con los nuevos detalles.",
            "new_date": request.new_date,
            "new_schedule": request.new_schedule,
            "new_time": request.new_time,
            "reschedule_count": reschedule_count + 1,
            "previous_date": current_appointment["date"],
            "previous_time": current_appointment["time"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al reagendar: {str(e)}")


@router.get("/reschedule/{token}")
async def get_reschedule_info(token: str):
    """Get appointment info for reschedule page using token"""
    try:
        appointment = await db.appointments.find_one({
            "reschedule_token": token,
            "status": "confirmed"
        })

        if not appointment:
            raise HTTPException(
                status_code=404,
                detail="No se encontró la cita o el enlace ha expirado."
            )

        reschedule_count = appointment.get('reschedule_count', 0)
        if reschedule_count >= 1:
            raise HTTPException(
                status_code=403,
                detail="Ya has reagendado esta cita anteriormente. Solo se permite reagendar una vez."
            )

        mexico_tz = pytz.timezone('America/Mexico_City')
        now_mexico = datetime.now(mexico_tz)

        appointment_datetime_str = f"{appointment['date']} {appointment['time']}"
        appointment_datetime = mexico_tz.localize(
            datetime.strptime(appointment_datetime_str, "%Y-%m-%d %H:%M")
        )

        hours_until_appointment = (appointment_datetime - now_mexico).total_seconds() / 3600

        if hours_until_appointment < 24:
            raise HTTPException(
                status_code=403,
                detail="No es posible reagendar con menos de 24 horas de anticipación. Por favor contáctanos por WhatsApp."
            )

        return {
            "success": True,
            "appointment": {
                "name": appointment["name"],
                "service": appointment["service"],
                "current_date": appointment["date"],
                "current_time": appointment["time"],
                "current_schedule": appointment["schedule"],
                "reschedule_count": reschedule_count,
                "can_reschedule": True
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting reschedule info: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener información de la cita.")


@router.put("/reschedule/{token}")
async def reschedule_by_token(token: str, request: TokenRescheduleRequest):
    """Reschedule appointment using token (self-service)"""
    try:
        appointment = await db.appointments.find_one({
            "reschedule_token": token,
            "status": "confirmed"
        })

        if not appointment:
            raise HTTPException(
                status_code=404,
                detail="No se encontró la cita o el enlace ha expirado."
            )

        reschedule_count = appointment.get('reschedule_count', 0)
        if reschedule_count >= 1:
            raise HTTPException(
                status_code=403,
                detail="Ya has reagendado esta cita anteriormente. Solo se permite reagendar una vez."
            )

        mexico_tz = pytz.timezone('America/Mexico_City')
        now_mexico = datetime.now(mexico_tz)

        appointment_datetime_str = f"{appointment['date']} {appointment['time']}"
        appointment_datetime = mexico_tz.localize(
            datetime.strptime(appointment_datetime_str, "%Y-%m-%d %H:%M")
        )

        hours_until_appointment = (appointment_datetime - now_mexico).total_seconds() / 3600

        if hours_until_appointment < 24:
            raise HTTPException(
                status_code=403,
                detail="No es posible reagendar con menos de 24 horas de anticipación. Por favor contáctanos por WhatsApp."
            )

        if not is_valid_appointment_date(request.new_date):
            raise HTTPException(
                status_code=400,
                detail="La nueva fecha debe ser al menos 48 horas después de ahora y en día laboral (Lunes-Viernes)"
            )

        if not is_business_hours(request.new_date, request.new_time):
            raise HTTPException(
                status_code=400,
                detail="La nueva cita debe ser de Lunes a Viernes, entre 9:00-12:00 AM o 4:00-7:00 PM"
            )

        existing = await db.appointments.find_one({
            "tenant_id": appointment.get("tenant_id", DEFAULT_TENANT_ID),
            "date": request.new_date,
            "time": request.new_time,
            "status": "confirmed"
        })

        if existing:
            raise HTTPException(
                status_code=400,
                detail="El nuevo horario ya está ocupado. Por favor selecciona otro."
            )

        previous_date = appointment["date"]
        previous_time = appointment["time"]
        previous_schedule = appointment["schedule"]

        update_result = await db.appointments.update_one(
            {"_id": appointment["_id"]},
            {
                "$set": {
                    "date": request.new_date,
                    "schedule": request.new_schedule,
                    "time": request.new_time,
                    "reschedule_count": reschedule_count + 1,
                    "rescheduled_at": datetime.now(timezone.utc).isoformat(),
                    "previous_date": previous_date,
                    "previous_time": previous_time,
                    "previous_schedule": previous_schedule
                }
            }
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=500,
                detail="Error al actualizar la cita. Inténtalo nuevamente."
            )

        updated_appointment = await db.appointments.find_one({"_id": appointment["_id"]})

        if updated_appointment:
            try:
                await send_confirmation_email(
                    updated_appointment["customer_email"],
                    updated_appointment
                )
                await create_google_calendar_event(updated_appointment)

                try:
                    await send_whatsapp_confirmation(updated_appointment)
                except Exception as whatsapp_error:
                    print(f"⚠️ WhatsApp notification failed: {whatsapp_error}")

                print(f"✅ Self-service reschedule successful for {updated_appointment['customer_email']}")

            except Exception as notification_error:
                print(f"⚠️ Reschedule successful but notification failed: {notification_error}")

        return {
            "success": True,
            "message": "¡Cita reagendada exitosamente!",
            "new_date": request.new_date,
            "new_schedule": request.new_schedule,
            "new_time": request.new_time,
            "previous_date": previous_date,
            "previous_time": previous_time
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in self-service reschedule: {e}")
        raise HTTPException(status_code=500, detail=f"Error al reagendar: {str(e)}")
