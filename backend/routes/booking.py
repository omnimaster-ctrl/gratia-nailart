"""
Booking creation, holds, payments, and VIP bypass routes for La Pop Nails.
"""

import os
import uuid
import json
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from database import db
from notification_service import create_notification
from tenant import DEFAULT_TENANT_ID
from scheduling import is_valid_appointment_date, is_business_hours, derive_schedule, ensure_utc_aware, PENDING_PAYMENT_EXPIRY_MINUTES
from models import PaymentRequest, BypassBookingRequest
from email_service import send_confirmation_email, send_owner_appointment_email
from calendar_service import create_google_calendar_event
from whatsapp_service import send_whatsapp_confirmation
from mercadopago_service import create_preference as create_mp_preference, get_payment_info
from discount_service import validate_discount, redeem_discount_atomic, DiscountValidationRequest
from phone_utils import normalize_phone

router = APIRouter(prefix="/api", tags=["booking"])


async def send_whatsapp_with_logging(phone: str, appointment_data: dict):
    """Wrapper to log WhatsApp errors in background tasks"""
    try:
        result = await send_whatsapp_confirmation(phone, appointment_data)
        if result:
            print(f"✅ WhatsApp confirmation sent successfully to {phone}")
        else:
            print(f"⚠️ WhatsApp confirmation failed for {phone}")
    except Exception as e:
        print(f"❌ WhatsApp confirmation error for {phone}: {e}")
        import traceback
        traceback.print_exc()


HOLD_DURATION_MINUTES = 15


@router.post("/booking/hold")
async def create_booking_hold(request: Request):
    """Create a temporary hold on a schedule block, identified by phone number."""
    try:
        data = await request.json()
        date = data.get("date")
        phone = data.get("phone", "")
        time_str = data.get("time", "")

        if not date:
            raise HTTPException(status_code=400, detail="Date required")

        clean_phone = normalize_phone(phone) if phone else ""
        schedule = derive_schedule(time_str) if time_str else "morning"

        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=HOLD_DURATION_MINUTES)

        # Check for existing active hold on this date+schedule
        existing_hold = await db.booking_holds.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": date,
            "schedule": schedule,
        })

        if existing_hold and existing_hold.get("expires_at"):
            hold_expired = ensure_utc_aware(existing_hold["expires_at"]) < now
            existing_phone = existing_hold.get("phone", "")

            if not hold_expired and clean_phone and existing_phone and existing_phone != clean_phone:
                remaining = (ensure_utc_aware(existing_hold["expires_at"]) - now).total_seconds() / 60
                return JSONResponse(
                    status_code=409,
                    content={
                        "detail": "Este horario está temporalmente reservado",
                        "remaining_minutes": round(remaining, 1),
                        "schedule": schedule,
                    },
                )

        hold_info = {
            "date": date,
            "schedule": schedule,
            "phone": clean_phone,
            "tenant_id": DEFAULT_TENANT_ID,
            "created_at": now,
            "expires_at": expires_at,
        }

        await db.booking_holds.update_one(
            {"tenant_id": DEFAULT_TENANT_ID, "date": date, "schedule": schedule},
            {"$set": hold_info},
            upsert=True,
        )

        return {
            "date": date,
            "schedule": schedule,
            "phone": clean_phone,
            "created_at": hold_info["created_at"].isoformat(),
            "expires_at": expires_at.isoformat(),
            "duration_minutes": HOLD_DURATION_MINUTES,
        }
    except HTTPException:
        raise
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=f"Error creating hold: {str(e)}")


@router.get("/booking/hold/status/{date}")
async def get_hold_status(date: str, phone: str = "", schedule: str = ""):
    """Check hold status for a date (optionally filtered by schedule block)."""
    try:
        clean_phone = normalize_phone(phone) if phone else ""
        now = datetime.now(timezone.utc)

        query = {"tenant_id": DEFAULT_TENANT_ID, "date": date, "expires_at": {"$gt": now}}
        if schedule:
            query["schedule"] = schedule

        holds = await db.booking_holds.find(query).to_list(length=10)

        if not holds:
            return {"active": False, "is_owner": False, "expires_at": None, "remaining_minutes": 0, "schedule": schedule or None}

        # If schedule specified, return single hold status
        if schedule and holds:
            hold = holds[0]
            remaining = (ensure_utc_aware(hold["expires_at"]) - now).total_seconds() / 60
            is_owner = bool(clean_phone and hold.get("phone") == clean_phone)
            return {
                "active": True,
                "is_owner": is_owner,
                "expires_at": ensure_utc_aware(hold["expires_at"]).isoformat(),
                "remaining_minutes": round(remaining, 1),
                "schedule": schedule,
            }

        # No schedule filter — return all active holds for the date
        result = {}
        for hold in holds:
            s = hold.get("schedule", "morning")
            remaining = (ensure_utc_aware(hold["expires_at"]) - now).total_seconds() / 60
            is_owner = bool(clean_phone and hold.get("phone") == clean_phone)
            result[s] = {
                "active": True,
                "is_owner": is_owner,
                "expires_at": ensure_utc_aware(hold["expires_at"]).isoformat(),
                "remaining_minutes": round(remaining, 1),
            }

        return {"holds": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking hold status: {str(e)}")


@router.delete("/booking/hold/{date}")
async def release_booking_hold(date: str, phone: str = "", schedule: str = ""):
    """Release a temporary hold on a booking slot. Requires phone ownership."""
    try:
        clean_phone = normalize_phone(phone) if phone else ""

        query = {"tenant_id": DEFAULT_TENANT_ID, "date": date}
        if schedule:
            query["schedule"] = schedule

        hold = await db.booking_holds.find_one(query)

        if not hold:
            return {"success": True, "message": "No hold found to release"}

        # Ownership check — if the hold has a phone, the caller must match
        if hold.get("phone") and clean_phone and hold["phone"] != clean_phone:
            raise HTTPException(status_code=403, detail="No autorizado para liberar esta reserva")

        await db.booking_holds.delete_one({"_id": hold["_id"]})
        return {"success": True, "message": f"Hold released for {date}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error releasing hold: {str(e)}")


@router.post("/create-mercadopago-preference")
async def create_mercadopago_payment(payment_request: PaymentRequest):
    """Create MercadoPago Checkout Pro preference"""
    try:
        if not is_valid_appointment_date(payment_request.appointment_data.date):
            raise HTTPException(status_code=400, detail="Fecha inválida")
        if not is_business_hours(payment_request.appointment_data.date, payment_request.appointment_data.time):
            raise HTTPException(status_code=400, detail="Horario inválido")

        existing = await db.appointments.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": payment_request.appointment_data.date,
            "time": payment_request.appointment_data.time,
            "status": "confirmed"
        })
        if existing:
            raise HTTPException(status_code=400, detail="Horario ocupado")

        appointment_id = str(uuid.uuid4())
        reschedule_token = str(uuid.uuid4())

        tenant_settings = await db.tenant_settings.find_one({"tenant_id": DEFAULT_TENANT_ID})
        anticipo_amount = float(tenant_settings.get("anticipo_amount", 250)) if tenant_settings else 250.00

        preference = create_mp_preference(
            appointment_id=appointment_id,
            customer_name=payment_request.appointment_data.name,
            customer_email=payment_request.customer_email,
            customer_phone=payment_request.appointment_data.phone,
            service_name=payment_request.appointment_data.service,
            amount=anticipo_amount,
            frontend_url=os.environ.get('FRONTEND_URL', 'https://lapopnails.mx')
        )

        try:
            await db.appointments.insert_one({
                "tenant_id": DEFAULT_TENANT_ID, "id": appointment_id,
                "name": payment_request.appointment_data.name, "phone": payment_request.appointment_data.phone,
                "service": payment_request.appointment_data.service, "date": payment_request.appointment_data.date,
                "time": payment_request.appointment_data.time, "schedule": payment_request.appointment_data.schedule,
                "customer_email": payment_request.customer_email, "status": "pending_payment",
                "mercadopago_preference_id": preference["preference_id"], "reschedule_token": reschedule_token,
                "created_at": datetime.now(timezone.utc).isoformat(), "reschedule_count": 0,
                **{k: v for k, v in payment_request.appointment_data.dict().items() if k not in ["name", "phone", "service", "date", "time", "schedule"]}
            })
        except DuplicateKeyError:
            raise HTTPException(status_code=409, detail="Este horario acaba de ser reservado. Por favor selecciona otro.")

        phone_digits = normalize_phone(payment_request.appointment_data.phone)
        await db.clients.update_one(
            {"tenant_id": DEFAULT_TENANT_ID, "phone": phone_digits},
            {"$set": {
                "phone": phone_digits, "name": payment_request.appointment_data.name,
                "email": payment_request.customer_email,
                **{k: payment_request.appointment_data.dict().get(k) for k in ["favoriteSnacks", "favoriteDrinks", "favoriteMovie", "favoriteSeries", "favoriteMusic", "birthday"] if payment_request.appointment_data.dict().get(k)},
                "updated_at": datetime.now(timezone.utc).isoformat()
            }, "$setOnInsert": {"tenant_id": DEFAULT_TENANT_ID, "created_at": datetime.now(timezone.utc).isoformat()}},
            upsert=True
        )

        return {
            "preference_id": preference["preference_id"],
            "appointment_id": appointment_id,
            "checkout_url": preference["init_point"]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ MercadoPago error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhooks/mercadopago")
async def handle_mercadopago_webhook(request: Request, background_tasks: BackgroundTasks):
    """Handle MercadoPago IPN webhooks"""
    try:
        mp_webhook_secret = os.environ.get("MP_WEBHOOK_SECRET", "")
        x_signature = request.headers.get("x-signature", "")
        x_request_id = request.headers.get("x-request-id", "")

        if mp_webhook_secret and x_signature:
            parts = {p.split("=", 1)[0].strip(): p.split("=", 1)[1].strip()
                     for p in x_signature.split(",") if "=" in p}
            ts = parts.get("ts", "")
            v1 = parts.get("v1", "")

            params_id = request.query_params.get("data.id", request.query_params.get("id", ""))

            manifest = f"id:{params_id};request-id:{x_request_id};ts:{ts};"

            computed = hmac.new(
                mp_webhook_secret.encode(),
                manifest.encode(),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(computed, v1):
                print(f"⚠️ MercadoPago webhook signature mismatch! Rejecting request.")
                return JSONResponse(status_code=401, content={"error": "Invalid signature"})
        elif mp_webhook_secret:
            print(f"⚠️ MercadoPago webhook missing x-signature header. Rejecting.")
            return JSONResponse(status_code=401, content={"error": "Missing signature"})
        else:
            raise HTTPException(status_code=500, detail="Webhook verification not configured")

        params = dict(request.query_params)
        topic = params.get("topic") or params.get("type")
        resource_id = params.get("id") or params.get("data.id")

        try:
            webhook_data = json.loads((await request.body()).decode())
            if not topic:
                topic = webhook_data.get("type") or webhook_data.get("topic")
            if not resource_id:
                resource_id = webhook_data.get("data", {}).get("id")
        except:
            webhook_data = {}

        print(f"📨 MercadoPago webhook: topic={topic}, id={resource_id}")

        if topic == "payment" and resource_id:
            try:
                payment_info = get_payment_info(resource_id)
                payment_status = payment_info.get("status")
                external_reference = payment_info.get("external_reference")

                print(f"💳 Payment {resource_id}: status={payment_status}, ref={external_reference}")

                if payment_status == "approved" and external_reference:
                    result = await db.appointments.update_one(
                        {"id": external_reference},
                        {"$set": {
                            "status": "confirmed",
                            "payment_id": str(resource_id),
                            "payment_method": "mercadopago",
                            "payment_status": "approved",
                            "amount_paid": payment_info.get("transaction_amount", 250),
                            "confirmed_at": datetime.now(timezone.utc).isoformat()
                        }}
                    )

                    if result.modified_count > 0:
                        apt = await db.appointments.find_one({"id": external_reference})
                        if apt:
                            print(f"✅ Payment confirmed for appointment {external_reference}")

                            await create_notification(
                                type="new_appointment",
                                title="Nueva cita confirmada",
                                body=f"{apt.get('name', 'Cliente')} - {apt.get('service', '')}, {apt.get('date', '')} {apt.get('time', '')}",
                                appointment_id=external_reference,
                            )

                            phone_number = apt.get("phone", "")
                            print(f"🔍 DEBUG - Phone from DB: '{phone_number}'")

                            background_tasks.add_task(send_confirmation_email, apt["customer_email"], apt)
                            background_tasks.add_task(create_google_calendar_event, apt)
                            background_tasks.add_task(send_owner_appointment_email, apt)

                            if phone_number:
                                background_tasks.add_task(send_whatsapp_with_logging, phone_number, apt)
                            else:
                                print(f"⚠️ WARNING: No phone number found for appointment {external_reference}")

                elif payment_status in ["rejected", "cancelled"]:
                    print(f"❌ Payment {payment_status}: {resource_id}")
                    if external_reference:
                        await db.appointments.update_one(
                            {"id": external_reference},
                            {"$set": {
                                "payment_status": payment_status,
                                "updated_at": datetime.now(timezone.utc).isoformat()
                            }}
                        )

                elif payment_status == "pending":
                    print(f"⏳ Payment pending: {resource_id}")

            except Exception as e:
                print(f"❌ Error fetching payment info: {e}")

        elif topic == "merchant_order" and resource_id:
            print(f"📦 Merchant order notification: {resource_id}")

        return {"status": "ok"}
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error"}


@router.post("/bookings/bypass")
async def create_bypass_booking(request: BypassBookingRequest):
    """
    Creates a CONFIRMED appointment directly for VIP clients with a valid waive_deposit code.
    Skips payment gateway entirely.
    """
    appt = request.appointment_data

    if not is_valid_appointment_date(appt.date):
         raise HTTPException(status_code=400, detail="Fecha no válida (debe ser día entre semana y con 48h de anticipación)")

    if not is_business_hours(appt.date, appt.time):
        raise HTTPException(status_code=400, detail="Horario fuera de servicio")

    existing = await db.appointments.find_one({
        "date": appt.date,
        "time": appt.time,
        "status": {"$in": ["confirmed", "pending_payment"]}
    })

    if existing:
        if existing['status'] == 'pending_payment':
            created = datetime.fromisoformat(existing['created_at'])
            if datetime.now(timezone.utc) - created < timedelta(minutes=PENDING_PAYMENT_EXPIRY_MINUTES):
                 raise HTTPException(status_code=409, detail="Este horario ya está ocupado")
        else:
             raise HTTPException(status_code=409, detail="Este horario ya está ocupado")

    validation_req = DiscountValidationRequest(
        code=request.coupon_code,
        cart_total=1000,
        service_id=appt.service
    )

    discount_result = await validate_discount(db, validation_req)

    if not discount_result.valid:
        raise HTTPException(status_code=400, detail=f"Cupón inválido: {discount_result.message}")

    if not discount_result.waive_deposit:
        raise HTTPException(status_code=403, detail="Este código no autoriza exentar el anticipo")

    redeemed = await redeem_discount_atomic(db, request.coupon_code, 250.0)
    if not redeemed:
        raise HTTPException(status_code=400, detail="El cupón se ha agotado o no se pudo canjear")

    appointment_doc = appt.dict()
    appointment_doc.update({
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "payment_id": "VIP_BYPASS",
        "payment_method": "coupon_bypass",
        "amount_paid": 0,
        "tenant_id": DEFAULT_TENANT_ID,
        "discount_code": request.coupon_code,
        "client_email": request.customer_email
    })

    try:
        result = await db.appointments.insert_one(appointment_doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Este horario acaba de ser reservado. Por favor selecciona otro.")

    notification_data = {
        **appointment_doc,
        "_id": str(result.inserted_id)
    }

    try:
        vip_phone = normalize_phone(appt.phone)
        await send_whatsapp_confirmation(vip_phone, notification_data)
        print(f"✅ VIP WhatsApp sent to {vip_phone}")
    except Exception as e:
        print(f"⚠️ Failed to send VIP WhatsApp: {e}")

    try:
        await send_confirmation_email(request.customer_email, notification_data)
        print(f"✅ VIP Email sent to {request.customer_email}")
    except Exception as e:
        print(f"⚠️ Failed to send VIP Email: {e}")

    return {"status": "success", "appointment_id": str(result.inserted_id), "message": "Cita VIP confirmada"}
