"""
Google Calendar OAuth and management routes for La Pop Nails.
"""

import os
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from google.oauth2 import service_account as google_service_account
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from database import db
from tenant import DEFAULT_TENANT_ID
from calendar_service import (
    _load_google_token,
    _save_google_token,
    create_google_calendar_event,
)

router = APIRouter(prefix="/api", tags=["calendar"])


@router.get("/auth/google-calendar")
async def initiate_google_calendar_auth():
    """Initiate Google Calendar OAuth2 authentication"""
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        CREDENTIALS_FILE = '/app/backend/client_secret.json'

        backend_url = os.environ.get('BACKEND_URL', 'http://localhost:8001')
        redirect_uri = f"{backend_url}/api/auth/google-calendar/callback"

        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )

        auth_url, _ = flow.authorization_url(prompt='consent')

        return {
            "auth_url": auth_url,
            "message": "Visit this URL to authorize Google Calendar access",
            "instructions": "After authorization, you'll be redirected to complete the setup",
            "redirect_uri": redirect_uri
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initiating Google Calendar auth: {str(e)}")


@router.get("/auth/google-calendar/callback")
async def google_calendar_callback(request: Request):
    """Handle Google Calendar OAuth2 callback"""
    try:
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        CREDENTIALS_FILE = '/app/backend/client_secret.json'

        code = request.query_params.get('code')
        if not code:
            raise HTTPException(status_code=400, detail="Authorization code not found")

        backend_url = os.environ.get('BACKEND_URL', 'http://localhost:8001')
        redirect_uri = f"{backend_url}/api/auth/google-calendar/callback"

        flow = Flow.from_client_secrets_file(
            CREDENTIALS_FILE,
            scopes=SCOPES,
            redirect_uri=redirect_uri
        )

        flow.fetch_token(code=code)
        creds = flow.credentials

        await _save_google_token(creds)

        service = build('calendar', 'v3', credentials=creds)
        calendar_list = service.calendarList().list().execute()

        print(f"✅ Google Calendar OAuth2 completed successfully!")
        print(f"   📅 Found {len(calendar_list.get('items', []))} calendars")

        pending_events = await db.calendar_events.find({"status": "pending_oauth"}).to_list(length=100)

        created_count = 0
        for pending_event in pending_events:
            try:
                event_details = pending_event["event_details"]
                cal_id = os.environ.get('GOOGLE_CALENDAR_ID', 'primary')
                created_event = service.events().insert(calendarId=cal_id, body=event_details, sendUpdates='none').execute()

                await db.calendar_events.update_one(
                    {"_id": pending_event["_id"]},
                    {
                        "$set": {
                            "google_event_id": created_event.get('id'),
                            "event_link": created_event.get('htmlLink'),
                            "status": "created",
                            "completed_at": datetime.now(timezone.utc).isoformat()
                        }
                    }
                )

                created_count += 1
                print(f"   ✅ Created pending event for appointment {pending_event['appointment_id']}")

            except Exception as event_error:
                print(f"   ❌ Failed to create pending event: {event_error}")
                await db.calendar_events.update_one(
                    {"_id": pending_event["_id"]},
                    {
                        "$set": {
                            "status": "creation_failed",
                            "error": str(event_error),
                            "completed_at": datetime.now(timezone.utc).isoformat()
                        }
                    }
                )

        return JSONResponse(
            status_code=200,
            content={
                "message": "Google Calendar integration completed successfully! ✅",
                "calendars_found": len(calendar_list.get('items', [])),
                "pending_events_created": created_count,
                "status": "ready",
                "next_step": "Calendar integration is now active for new appointments"
            }
        )

    except Exception as e:
        print(f"❌ Google Calendar callback error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error completing Google Calendar auth: {str(e)}")


@router.get("/calendar/status")
async def get_calendar_integration_status():
    """Get Google Calendar integration status"""
    try:
        creds = await _load_google_token()

        if not creds:
            return {
                "status": "not_configured",
                "message": "Google Calendar not configured. Authentication needed.",
                "auth_url": "/api/auth/google-calendar"
            }

        is_service_account = isinstance(creds, google_service_account.Credentials)

        if not is_service_account and not creds.valid:
            return {
                "status": "authentication_needed",
                "message": "Google Calendar credentials expired. Re-authentication needed.",
                "auth_url": "/api/auth/google-calendar"
            }

        service = build('calendar', 'v3', credentials=creds)
        cal_id = os.environ.get('GOOGLE_CALENDAR_ID', 'primary')
        calendar_info = service.calendars().get(calendarId=cal_id).execute()

        total_events = await db.calendar_events.count_documents({})
        created_events = await db.calendar_events.count_documents({"status": "created"})
        pending_events = await db.calendar_events.count_documents({"status": "pending_oauth"})
        failed_events = await db.calendar_events.count_documents({"status": "creation_failed"})

        return {
            "status": "active",
            "auth_method": "service_account" if is_service_account else "oauth",
            "calendar_name": calendar_info.get('summary', cal_id),
            "statistics": {
                "total_events": total_events,
                "created_events": created_events,
                "pending_events": pending_events,
                "failed_events": failed_events
            },
            "message": "Google Calendar integration is active and working"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error checking calendar status: {str(e)}",
            "auth_url": "/api/auth/google-calendar"
        }


@router.post("/management/sync-calendar-missing")
async def management_sync_missing_to_calendar(secret: str = "", from_date: str = None):
    """
    One-time management endpoint to sync confirmed appointments missing from calendar.
    Protected by secret query parameter.
    """
    expected_secret = os.environ.get("MANAGEMENT_SECRET", "popnails-sync-2026")
    if secret != expected_secret:
        raise HTTPException(status_code=403, detail="Forbidden")

    start_date = from_date if from_date else datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Management sync: Looking for confirmed appointments from {start_date} onwards...")

    appointments = await db.appointments.find({
        "status": "confirmed",
        "date": {"$gte": start_date}
    }).to_list(100)

    print(f"📋 Found {len(appointments)} confirmed appointments")

    synced = []
    already_synced = []
    failed = []

    for apt in appointments:
        apt_id = str(apt["_id"])
        name = apt.get("name", "Unknown")
        date = apt.get("date", "?")
        time_str = apt.get("time", "?")

        existing = await db.calendar_events.find_one({
            "appointment_id": apt_id,
            "status": "created"
        })

        if existing:
            print(f"  ✅ Already synced: {name} on {date} {time_str}")
            already_synced.append({"id": apt_id, "name": name, "date": date})
            continue

        print(f"  🔄 Syncing: {name} on {date} {time_str}")
        apt_data = {
            "id": apt_id,
            "name": apt.get("name"),
            "phone": apt.get("phone"),
            "customer_email": apt.get("customer_email"),
            "date": apt.get("date"),
            "time": apt.get("time"),
            "service": apt.get("service"),
            "retiro": apt.get("retiro"),
            "manicurista": apt.get("manicurista"),
            "notes": apt.get("notes"),
            "tenant_id": apt.get("tenant_id", DEFAULT_TENANT_ID),
        }

        result = await create_google_calendar_event(apt_data)

        if result is True:
            print(f"  ✅ Synced successfully!")
            synced.append({"id": apt_id, "name": name, "date": date})
        else:
            print(f"  ❌ Failed to sync")
            failed.append({"id": apt_id, "name": name, "date": date})

    return {
        "synced": synced,
        "already_synced": already_synced,
        "failed": failed,
        "summary": {
            "synced_count": len(synced),
            "already_synced_count": len(already_synced),
            "failed_count": len(failed)
        }
    }
