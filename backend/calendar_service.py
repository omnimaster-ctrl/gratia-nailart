"""
Google Calendar integration for La Pop Nails.
Handles OAuth token management, event creation, and event deletion.
"""

import os
import json
import base64
import pickle
from datetime import datetime, timedelta, timezone

import pytz
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account as google_service_account
from googleapiclient.discovery import build

from database import db


def _load_google_service_account():
    """Load Google Service Account credentials from env var. Never expires."""
    try:
        sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not sa_json:
            return None
        sa_info = json.loads(sa_json)
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = google_service_account.Credentials.from_service_account_info(
            sa_info, scopes=SCOPES
        )
        return creds
    except Exception as e:
        print(f"⚠️  Failed to load Google Service Account: {e}")
        return None


async def _load_google_token():
    """Load Google credentials. Prefers service account; falls back to OAuth token in MongoDB."""
    creds = _load_google_service_account()
    if creds:
        return creds

    try:
        doc = await db.system_config.find_one({"key": "google_calendar_token"})
        if doc and doc.get("token_json"):
            token_data = doc["token_json"]
            creds = Credentials(
                token=token_data.get("token"),
                refresh_token=token_data.get("refresh_token"),
                token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
                client_id=token_data.get("client_id"),
                client_secret=token_data.get("client_secret"),
                scopes=token_data.get("scopes"),
            )
        elif doc and doc.get("token_b64"):
            print("⚠️ Loading legacy pickle token — will migrate to JSON on next save")
            creds = pickle.loads(base64.b64decode(doc["token_b64"]))
        else:
            return None

        if creds and not creds.valid and creds.expired and creds.refresh_token:
            print("🔄 Auto-refreshing expired Google Calendar token...")
            creds.refresh(GoogleRequest())
            await _save_google_token(creds)
            print("✅ Google token refreshed and saved (JSON format)")
        return creds
    except Exception as e:
        print(f"⚠️  Failed to load Google token from DB: {e}")
    return None


async def _save_google_token(creds):
    """Save Google OAuth token to MongoDB as JSON (survives Railway redeploys)."""
    try:
        token_json = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": list(creds.scopes) if creds.scopes else None,
        }
        await db.system_config.update_one(
            {"key": "google_calendar_token"},
            {"$set": {
                "token_json": token_json,
                "token_b64": None,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }},
            upsert=True,
        )
        print("✅ Google token saved to MongoDB (JSON)")
    except Exception as e:
        print(f"❌ Failed to save Google token to DB: {e}")


async def create_google_calendar_event(appointment_data: dict):
    """Create Google Calendar event using OAuth2 credentials"""
    try:
        print(f"🔄 Starting Google Calendar integration for appointment {appointment_data.get('id', 'N/A')}")

        SCOPES = ['https://www.googleapis.com/auth/calendar']

        creds = await _load_google_token()

        is_service_account = isinstance(creds, google_service_account.Credentials) if creds else False
        creds_valid = is_service_account or (creds and creds.valid)

        if not creds_valid:
            if not creds:
                print("🔄 Starting OAuth2 flow for Google Calendar...")
                print("📅 Google Calendar OAuth2 setup needed. Event details prepared:")

                appointment_datetime = datetime.strptime(
                    f"{appointment_data['date']} {appointment_data['time']}",
                    "%Y-%m-%d %H:%M"
                )
                end_datetime = appointment_datetime + timedelta(hours=1, minutes=30)

                event_details = {
                    'summary': f"💅 La Pop Nails - {appointment_data['service']}",
                    'description': f"""
🎯 CITA CONFIRMADA CON ANTICIPO PAGADO ✅

👤 Cliente: {appointment_data['name']}
📱 Teléfono: {appointment_data['phone']}
📧 Email: {appointment_data.get('customer_email', 'No proporcionado')}
💅 Servicio: {appointment_data['service']}
💰 Anticipo: $250 MXN ✅ PAGADO

{f"🔄 Retiro requerido: Sí" if appointment_data.get('retiro') else ''}
{f"💡 Ideas proporcionadas: {len(appointment_data.get('imagenes', []))} imágenes" if appointment_data.get('tieneIdeas') else ''}
{f"🎨 Libertad artística: Sí" if appointment_data.get('libertadArtistica') else ''}
{f"📝 Notas especiales: {appointment_data['notes']}" if appointment_data.get('notes') else ''}

🏷️  Estado: CONFIRMADA
⚡ Creado automáticamente por sistema La Pop Nails
📞 Instagram: @___lapopnails

💼 ID de cita: {appointment_data.get('id', 'N/A')}
🕐 Duración estimada: 1.5 horas
                    """.strip(),
                    'start': {
                        'dateTime': appointment_datetime.isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'end': {
                        'dateTime': end_datetime.isoformat(),
                        'timeZone': 'America/Mexico_City',
                    },
                    'attendees': [
                        {
                            'email': appointment_data.get('customer_email', ''),
                            'displayName': appointment_data['name'],
                            'responseStatus': 'accepted'
                        },
                        {
                            'email': os.environ.get('GOOGLE_CALENDAR_EMAIL', 'lapopnails.28@gmail.com'),
                            'displayName': 'La Pop Nails',
                            'responseStatus': 'accepted'
                        }
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 60},
                            {'method': 'popup', 'minutes': 15},
                        ],
                    },
                    'visibility': 'private',
                    'colorId': '10',
                }

                print(f"📅 CALENDAR EVENT PREPARED:")
                print(f"   📋 Title: {event_details['summary']}")
                print(f"   👤 Cliente: {appointment_data['name']}")
                print(f"   📧 Email: {appointment_data.get('customer_email', 'N/A')}")
                print(f"   📅 Fecha/Hora: {appointment_data['date']} at {appointment_data['time']}")
                print(f"   💅 Servicio: {appointment_data['service']}")
                print(f"   💰 Anticipo: PAGADO ✅")
                print(f"   🔔 Recordatorios: 1 día, 1 hora y 15 min antes")
                print(f"   ⏰ Duración: 1.5 horas")
                print(f"   📞 Invitados: Cliente + La Pop Nails")

                await db.calendar_events.insert_one({
                    "appointment_id": appointment_data.get('id'),
                    "event_details": event_details,
                    "status": "pending_oauth",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "customer_email": appointment_data.get('customer_email')
                })

                print("📋 Event details stored in database for OAuth completion")
                return True

        if creds_valid:
            print("✅ Valid Google Calendar credentials found")
            service = build('calendar', 'v3', credentials=creds)

            appointment_datetime = datetime.strptime(
                f"{appointment_data['date']} {appointment_data['time']}",
                "%Y-%m-%d %H:%M"
            )
            end_datetime = appointment_datetime + timedelta(hours=1, minutes=30)

            event = {
                'summary': f"💅 La Pop Nails - {appointment_data['service']}",
                'description': f"""
🎯 CITA CONFIRMADA CON ANTICIPO PAGADO ✅

👤 Cliente: {appointment_data['name']}
📱 Teléfono: {appointment_data['phone']}
📧 Email: {appointment_data.get('customer_email', 'No proporcionado')}
💅 Servicio: {appointment_data['service']}
💰 Anticipo: $250 MXN ✅ PAGADO

{f"🔄 Retiro requerido: Sí" if appointment_data.get('retiro') else ''}
{f"💡 Ideas proporcionadas: {len(appointment_data.get('imagenes', []))} imágenes" if appointment_data.get('tieneIdeas') else ''}
{f"🎨 Libertad artística: Sí" if appointment_data.get('libertadArtistica') else ''}
{f"📝 Notas especiales: {appointment_data['notes']}" if appointment_data.get('notes') else ''}

🏷️  Estado: CONFIRMADA
⚡ Creado automáticamente por sistema La Pop Nails
📞 Instagram: @___lapopnails

💼 ID de cita: {appointment_data.get('id', 'N/A')}
🕐 Duración estimada: 1.5 horas
                """.strip(),
                'start': {
                    'dateTime': appointment_datetime.isoformat(),
                    'timeZone': 'America/Mexico_City',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'America/Mexico_City',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 60},
                        {'method': 'popup', 'minutes': 15},
                    ],
                },
                'visibility': 'private',
                'colorId': '10',
            }

            if not is_service_account:
                event['attendees'] = [
                    {
                        'email': appointment_data.get('customer_email', ''),
                        'displayName': appointment_data['name'],
                        'responseStatus': 'accepted'
                    },
                    {
                        'email': os.environ.get('GOOGLE_CALENDAR_EMAIL', 'lapopnails.28@gmail.com'),
                        'displayName': 'La Pop Nails',
                        'responseStatus': 'accepted'
                    }
                ]

            try:
                cal_id = os.environ.get('GOOGLE_CALENDAR_ID', 'primary')
                created_event = service.events().insert(calendarId=cal_id, body=event, sendUpdates='none').execute()

                await db.calendar_events.insert_one({
                    "appointment_id": appointment_data.get('id'),
                    "google_event_id": created_event.get('id'),
                    "event_link": created_event.get('htmlLink'),
                    "status": "created",
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "customer_email": appointment_data.get('customer_email')
                })

                print(f"✅ GOOGLE CALENDAR EVENT CREATED SUCCESSFULLY!")
                print(f"   📅 Event ID: {created_event.get('id')}")
                print(f"   🔗 Event Link: {created_event.get('htmlLink')}")
                print(f"   👤 Cliente: {appointment_data['name']}")
                print(f"   📅 Fecha: {appointment_data['date']} {appointment_data['time']}")
                print(f"   💅 Servicio: {appointment_data['service']}")

                return True

            except Exception as creation_error:
                print(f"❌ Failed to create Google Calendar event: {creation_error}")

                await db.calendar_events.insert_one({
                    "appointment_id": appointment_data.get('id'),
                    "status": "creation_failed",
                    "error": str(creation_error),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "customer_email": appointment_data.get('customer_email')
                })

                return False

        return True

    except Exception as e:
        print(f"❌ Failed to process Google Calendar integration: {str(e)}")

        try:
            await db.calendar_events.insert_one({
                "appointment_id": appointment_data.get('id'),
                "status": "integration_error",
                "error": str(e),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "customer_email": appointment_data.get('customer_email')
            })
        except:
            pass

        return False


async def delete_google_calendar_event(appointment_id: str):
    """Delete Google Calendar event when appointment is cancelled"""
    try:
        print(f"🔄 Deleting Google Calendar event for appointment {appointment_id}")

        calendar_event = await db.calendar_events.find_one({
            "appointment_id": appointment_id,
            "status": "created"
        })

        if not calendar_event:
            print(f"⚠️  No Google Calendar event found for appointment {appointment_id}")
            return False

        google_event_id = calendar_event.get('google_event_id')
        if not google_event_id:
            print(f"⚠️  No google_event_id found in calendar record")
            return False

        creds = await _load_google_token()

        is_sa = isinstance(creds, google_service_account.Credentials) if creds else False
        creds_ok = is_sa or (creds and creds.valid)

        if not creds_ok:
            print("⚠️  Google Calendar credentials not available or expired")
            return False

        print("✅ Valid Google Calendar credentials found")
        service = build('calendar', 'v3', credentials=creds)

        try:
            service.events().delete(
                calendarId=os.environ.get('GOOGLE_CALENDAR_ID', 'primary'),
                eventId=google_event_id,
                sendUpdates='all'
            ).execute()

            await db.calendar_events.update_one(
                {"_id": calendar_event["_id"]},
                {"$set": {"status": "cancelled", "cancelled_at": datetime.now(timezone.utc).isoformat()}}
            )

            print(f"✅ GOOGLE CALENDAR EVENT DELETED SUCCESSFULLY!")
            print(f"   📅 Event ID: {google_event_id}")
            return True

        except Exception as delete_error:
            print(f"❌ Failed to delete Google Calendar event: {delete_error}")
            await db.calendar_events.update_one(
                {"_id": calendar_event["_id"]},
                {"$set": {"status": "deletion_failed", "deletion_error": str(delete_error), "deletion_attempted_at": datetime.now(timezone.utc).isoformat()}}
            )
            return False

    except Exception as e:
        print(f"❌ Failed to delete Google Calendar event: {str(e)}")
        return False
