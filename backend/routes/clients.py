"""
Client lookup routes for La Pop Nails.
Includes rate limiting for PII protection.
"""

from collections import defaultdict
import time as _time
from fastapi import APIRouter, HTTPException, Request

from database import db
from tenant import DEFAULT_TENANT_ID
from phone_utils import normalize_phone

router = APIRouter(prefix="/api", tags=["clients"])

# Rate limiting state
_rate_limit_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX_REQUESTS = 10


def _check_rate_limit(client_ip: str) -> bool:
    """Returns True if request is allowed, False if rate-limited."""
    now = _time.time()
    window_start = now - RATE_LIMIT_WINDOW
    _rate_limit_store[client_ip] = [
        t for t in _rate_limit_store[client_ip] if t > window_start
    ]
    if len(_rate_limit_store[client_ip]) >= RATE_LIMIT_MAX_REQUESTS:
        return False
    _rate_limit_store[client_ip].append(now)
    return True


@router.get("/client/lookup/{phone}")
async def lookup_client_by_phone(phone: str, request: Request):
    """
    Look up a returning client by their phone number.
    Returns their saved preferences and info to pre-fill the booking form.
    """
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Demasiadas solicitudes. Intenta de nuevo en un minuto.")

    try:
        phone_10 = normalize_phone(phone)

        client_record = await db.clients.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "phone": phone_10
        })

        phone_patterns = [
            phone_10,
            f"+52{phone_10}",
            f"+521{phone_10}",
        ]

        appointment = await db.appointments.find_one(
            {
                "tenant_id": DEFAULT_TENANT_ID,
                "phone": {"$in": phone_patterns},
                "status": {"$in": ["confirmed", "pending_payment"]}
            },
            sort=[("created_at", -1)]
        )
        appointment_data = appointment if appointment else None

        if not client_record and not appointment_data:
            return {
                "found": False,
                "message": "Cliente no encontrado"
            }

        name = ""
        email = ""

        if client_record:
            name = client_record.get("name", "")
            email = client_record.get("email", "")
        if not name and appointment_data:
            name = appointment_data.get("name", "")
        if not email and appointment_data:
            email = appointment_data.get("customer_email", "")

        def get_pref(key):
            if client_record and client_record.get(key):
                return client_record.get(key)
            if appointment_data and appointment_data.get(key):
                return appointment_data.get(key)
            return ""

        favoriteSnacks = get_pref("favoriteSnacks")
        favoriteDrinks = get_pref("favoriteDrinks")
        favoriteMovie = get_pref("favoriteMovie")
        favoriteSeries = get_pref("favoriteSeries")
        favoriteMusic = get_pref("favoriteMusic")
        birthday = get_pref("birthday")

        print(f"🔍 Client lookup for {phone_10}:")
        print(f"   - clients collection: {'found' if client_record else 'not found'}")
        print(f"   - appointments: {'found' if appointment_data else 'not found'}")
        print(f"   - Preferences: snacks={favoriteSnacks}, drinks={favoriteDrinks}, birthday={birthday}")

        appointment_count = await db.appointments.count_documents({
            "tenant_id": DEFAULT_TENANT_ID,
            "phone": {"$in": phone_patterns},
            "status": "confirmed"
        })

        return {
            "found": True,
            "isReturningClient": True,
            "name": name,
            "email": email,
            "phone": phone_10,
            "favoriteSnacks": favoriteSnacks,
            "favoriteDrinks": favoriteDrinks,
            "favoriteMovie": favoriteMovie,
            "favoriteSeries": favoriteSeries,
            "favoriteMusic": favoriteMusic,
            "birthday": birthday,
            "appointmentCount": appointment_count,
            "lastVisit": appointment_data.get("date", "") if appointment_data else "",
            "message": "¡Bienvenida de vuelta! 💅"
        }

    except Exception as e:
        print(f"Error looking up client: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "found": False,
            "message": "Error al buscar cliente"
        }
