"""
Admin appointment management — weekly view, cancel, archive, delete, calendar sync.
"""

from datetime import datetime, timedelta, date, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from database import db
from auth import get_current_admin
from tenant import DEFAULT_TENANT_ID
from scheduling import get_service_duration, get_service_price
from models import CancelAppointmentRequest

router = APIRouter(tags=["admin-appointments"])


@router.get("/appointments/weekly")
async def get_weekly_appointments(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    include_archived: bool = False,
    admin: dict = Depends(get_current_admin)
):
    """Get appointments for a date range."""
    if start_date:
        try:
            week_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

    if end_date:
        try:
            week_end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD")
    else:
        week_end = week_start + timedelta(days=4)

    query_filter = {
        "tenant_id": DEFAULT_TENANT_ID,
        "date": {
            "$gte": week_start.isoformat(),
            "$lte": week_end.isoformat()
        }
    }

    if not include_archived:
        query_filter["$or"] = [
            {"is_archived": {"$exists": False}},
            {"is_archived": False}
        ]

    appointments_cursor = db.appointments.find(query_filter).sort("date", 1).sort("time", 1)
    appointments_list = await appointments_cursor.to_list(length=100)

    formatted_appointments = []
    stats = {
        "total_appointments": 0,
        "confirmed": 0,
        "pending": 0,
        "cancelled": 0
    }

    for apt in appointments_list:
        client_record = await db.clients.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "phone": apt.get("phone", "").replace("+52", "")[-10:]
        })

        is_returning = client_record is not None and client_record.get("appointment_count", 0) > 1

        formatted_apt = {
            "id": str(apt["_id"]),
            "date": apt.get("date"),
            "time": apt.get("time"),
            "schedule": apt.get("schedule", ""),
            "status": apt.get("status", "pending_payment"),
            "client": {
                "name": apt.get("name"),
                "phone": apt.get("phone"),
                "email": apt.get("customer_email"),
                "is_returning": is_returning
            },
            "service": apt.get("service"),
            "service_duration": get_service_duration(apt.get("service")),
            "preferences": {
                "favoriteSnacks": apt.get("favoriteSnacks"),
                "favoriteDrinks": apt.get("favoriteDrinks"),
                "favoriteMovie": apt.get("favoriteMovie"),
                "favoriteSeries": apt.get("favoriteSeries"),
                "favoriteMusic": apt.get("favoriteMusic"),
                "birthday": apt.get("birthday")
            } if apt.get("favoriteSnacks") or apt.get("favoriteDrinks") else None,
            "payment": {
                "deposit_paid": 250 if apt.get("status") == "confirmed" else 0,
                "total_estimated": get_service_price(apt.get("service")),
                "payment_id": apt.get("payment_id")
            },
            "created_at": apt.get("created_at", apt.get("confirmed_at", ""))
        }

        formatted_appointments.append(formatted_apt)

        stats["total_appointments"] += 1
        apt_status = apt.get("status", "pending_payment")
        if apt_status == "confirmed":
            stats["confirmed"] += 1
        elif apt_status == "cancelled":
            stats["cancelled"] += 1
        else:
            stats["pending"] += 1

    return {
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "appointments": formatted_appointments,
        "stats": stats
    }


@router.put("/appointments/{appointment_id}/cancel")
async def cancel_appointment(
    appointment_id: str,
    cancel_data: CancelAppointmentRequest,
    admin: dict = Depends(get_current_admin)
):
    """Cancel an appointment and send notifications to the client."""
    from bson import ObjectId

    try:
        apt_id = ObjectId(appointment_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid appointment ID"
        )

    appointment = await db.appointments.find_one({"_id": apt_id})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    if appointment.get("status") == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment is already cancelled"
        )

    client_phone = appointment.get("phone")
    client = None
    if client_phone:
        client = await db.clients.find_one({"phone": client_phone})

    update_data = {
        "status": "cancelled",
        "cancelled_at": datetime.now(timezone.utc).isoformat(),
        "cancelled_by": admin["email"],
        "cancellation_reason": cancel_data.reason
    }

    await db.appointments.update_one(
        {"_id": apt_id},
        {"$set": update_data}
    )

    try:
        from calendar_service import delete_google_calendar_event
        await delete_google_calendar_event(appointment_id)
        print(f"✅ Google Calendar event deleted for appointment {appointment_id}")
    except Exception as e:
        print(f"⚠️  Failed to delete Google Calendar event: {e}")

    if cancel_data.notify_client:
        from email_service import send_cancellation_email
        from whatsapp_service import send_whatsapp_cancellation

        notification_data = {
            "name": appointment.get("name", "Cliente"),
            "email": appointment.get("customer_email"),
            "phone": client_phone,
            "date": appointment.get("date"),
            "time": appointment.get("time"),
            "service": appointment.get("service"),
            "reason": cancel_data.reason
        }

        customer_email = appointment.get("customer_email")
        if customer_email:
            try:
                await send_cancellation_email(customer_email, notification_data)
            except Exception as e:
                print(f"❌ Failed to send cancellation email: {e}")

        if client_phone:
            try:
                await send_whatsapp_cancellation(client_phone, notification_data)
            except Exception as e:
                print(f"❌ Failed to send WhatsApp cancellation: {e}")

    return {
        "success": True,
        "message": "Appointment cancelled successfully",
        "appointment_id": appointment_id,
        "notifications_sent": cancel_data.notify_client
    }


@router.put("/appointments/{appointment_id}/archive")
async def archive_appointment(
    appointment_id: str,
    admin: dict = Depends(get_current_admin)
):
    """Archive a cancelled appointment to hide it from the main calendar view."""
    from bson import ObjectId

    try:
        apt_id = ObjectId(appointment_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid appointment ID"
        )

    appointment = await db.appointments.find_one({"_id": apt_id})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    if appointment.get("status") != "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only cancelled appointments can be archived"
        )

    await db.appointments.update_one(
        {"_id": apt_id},
        {"$set": {
            "is_archived": True,
            "archived_at": datetime.now(timezone.utc).isoformat(),
            "archived_by": admin["email"]
        }}
    )

    return {
        "success": True,
        "message": "Appointment archived successfully",
        "appointment_id": appointment_id
    }


@router.delete("/appointments/{appointment_id}")
async def delete_appointment(
    appointment_id: str,
    admin: dict = Depends(get_current_admin)
):
    """Permanently delete an archived cancelled appointment."""
    from bson import ObjectId

    try:
        apt_id = ObjectId(appointment_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid appointment ID"
        )

    appointment = await db.appointments.find_one({"_id": apt_id})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    if appointment.get("status") != "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only cancelled appointments can be deleted"
        )

    if not appointment.get("is_archived"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only archived appointments can be permanently deleted"
        )

    result = await db.appointments.delete_one({"_id": apt_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete appointment"
        )

    print(f"🗑️  Permanently deleted appointment {appointment_id} by {admin['email']}")

    return {
        "success": True,
        "message": "Appointment permanently deleted",
        "appointment_id": appointment_id
    }


@router.post("/appointments/{appointment_id}/sync-calendar")
async def sync_appointment_to_calendar(
    appointment_id: str,
    admin: dict = Depends(get_current_admin)
):
    """Manually sync an existing appointment to Google Calendar."""
    from bson import ObjectId
    from calendar_service import create_google_calendar_event

    try:
        apt_id = ObjectId(appointment_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid appointment ID"
        )

    appointment = await db.appointments.find_one({"_id": apt_id})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    existing_event = await db.calendar_events.find_one({
        "appointment_id": appointment_id,
        "status": "created"
    })
    if existing_event:
        return {
            "success": True,
            "message": "Calendar event already exists",
            "event_id": existing_event.get("google_event_id"),
            "event_link": existing_event.get("event_link")
        }

    apt_data = {
        "id": appointment_id,
        "name": appointment.get("name"),
        "phone": appointment.get("phone"),
        "customer_email": appointment.get("customer_email"),
        "date": appointment.get("date"),
        "time": appointment.get("time"),
        "service": appointment.get("service"),
        "retiro": appointment.get("retiro"),
        "tieneIdeas": appointment.get("tieneIdeas"),
        "imagenes": appointment.get("imagenes"),
        "libertadArtistica": appointment.get("libertadArtistica"),
        "notes": appointment.get("notes")
    }

    try:
        result = await create_google_calendar_event(apt_data)
        if result:
            event = await db.calendar_events.find_one({
                "appointment_id": appointment_id,
                "status": "created"
            })
            return {
                "success": True,
                "message": "Calendar event created successfully",
                "event_id": event.get("google_event_id") if event else None,
                "event_link": event.get("event_link") if event else None
            }
        else:
            return {
                "success": False,
                "message": "Failed to create calendar event - check server logs"
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating calendar event: {str(e)}"
        )


@router.post("/appointments/sync-all-missing")
async def sync_all_missing_to_calendar(
    admin: dict = Depends(get_current_admin)
):
    """Find all confirmed appointments without calendar events and sync them."""
    from calendar_service import create_google_calendar_event

    today = datetime.now().strftime("%Y-%m-%d")

    appointments = await db.appointments.find({
        "status": "confirmed",
        "date": {"$gte": today}
    }).to_list(100)

    synced = []
    already_synced = []
    failed = []

    for apt in appointments:
        apt_id = str(apt["_id"])

        existing = await db.calendar_events.find_one({
            "appointment_id": apt_id,
            "status": "created"
        })

        if existing:
            already_synced.append({
                "id": apt_id,
                "name": apt.get("name"),
                "date": apt.get("date")
            })
            continue

        apt_data = {
            "id": apt_id,
            "name": apt.get("name"),
            "phone": apt.get("phone"),
            "customer_email": apt.get("customer_email"),
            "date": apt.get("date"),
            "time": apt.get("time"),
            "service": apt.get("service"),
            "retiro": apt.get("retiro"),
            "tieneIdeas": apt.get("tieneIdeas"),
            "imagenes": apt.get("imagenes"),
            "libertadArtistica": apt.get("libertadArtistica"),
            "notes": apt.get("notes")
        }

        try:
            result = await create_google_calendar_event(apt_data)
            if result:
                synced.append({
                    "id": apt_id,
                    "name": apt.get("name"),
                    "date": apt.get("date")
                })
            else:
                failed.append({
                    "id": apt_id,
                    "name": apt.get("name"),
                    "date": apt.get("date"),
                    "error": "Calendar creation returned False"
                })
        except Exception as e:
            failed.append({
                "id": apt_id,
                "name": apt.get("name"),
                "date": apt.get("date"),
                "error": str(e)
            })

    return {
        "synced": synced,
        "already_synced": already_synced,
        "failed": failed,
        "summary": {
            "total_found": len(appointments),
            "newly_synced": len(synced),
            "already_had_events": len(already_synced),
            "failed": len(failed)
        }
    }
