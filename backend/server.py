"""
Gratia Nail Art API — Application entry point.
Creates the FastAPI app, configures middleware, registers routers, and starts background tasks.
"""

import os
import asyncio
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Setup Google Calendar credentials from environment variable
import base64
google_creds_b64 = os.environ.get('GOOGLE_CLIENT_SECRET_JSON')
if google_creds_b64:
    try:
        google_creds_json = base64.b64decode(google_creds_b64).decode('utf-8')
        os.makedirs('/app/backend', exist_ok=True)
        with open('/app/backend/client_secret.json', 'w') as f:
            f.write(google_creds_json)
        print("✅ Google Calendar credentials configured from environment")
    except Exception as e:
        print(f"⚠️ Failed to configure Google Calendar credentials: {e}")

from database import db
from tenant import ensure_default_tenant
from scheduling import PENDING_PAYMENT_EXPIRY_MINUTES

# Route modules
from routes.admin import router as admin_router
from routes.internal import router as internal_router
from routes.tenants import router as tenants_router
from routes.clients import router as clients_router
from routes.discounts import router as discounts_router
from routes.appointments import router as appointments_router
from routes.booking import router as booking_router
from routes.reschedule import router as reschedule_router
from routes.calendar import router as calendar_router

# =============================================================================
# APP CREATION
# =============================================================================

app = FastAPI(title="Gratia Nail Art API")

# =============================================================================
# CORS MIDDLEWARE
# =============================================================================

import json as _json

_origins_env = os.environ.get("ALLOWED_ORIGINS", "")
if _origins_env:
    ALLOWED_ORIGINS = _json.loads(_origins_env)
else:
    ALLOWED_ORIGINS = [
        "https://gratia-nailart-production.up.railway.app",
        "https://gratianailart.com",
        "https://www.gratianailart.com",
    ]

if os.environ.get("RAILWAY_ENVIRONMENT", "production") != "production":
    ALLOWED_ORIGINS += ["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ROUTER REGISTRATION
# =============================================================================

app.include_router(admin_router)
app.include_router(internal_router)
app.include_router(tenants_router)
app.include_router(clients_router)
app.include_router(discounts_router)
app.include_router(appointments_router)
app.include_router(booking_router)
app.include_router(reschedule_router)
app.include_router(calendar_router)

# =============================================================================
# BACKGROUND TASKS
# =============================================================================

async def run_expiration_monitor():
    """
    Background task that runs periodically to cancel expired pending appointments.
    This ensures database hygiene regardless of client interactions.
    """
    print("🛡️ Starting Expiration Monitor background task...")
    while True:
        try:
            expiry_threshold = datetime.now(timezone.utc) - timedelta(minutes=PENDING_PAYMENT_EXPIRY_MINUTES)

            query = {
                "status": "pending_payment",
                "created_at": {"$lt": expiry_threshold.isoformat()}
            }

            result = await db.appointments.update_many(
                query,
                {
                    "$set": {
                        "status": "cancelled",
                        "cancelled_reason": "auto_timeout_15min",
                        "cancelled_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )

            if result.modified_count > 0:
                print(f"🧹 Auto-cancelled {result.modified_count} expired pending appointments.")

        except Exception as e:
            print(f"❌ Error in expiration monitor: {e}")
            import traceback
            traceback.print_exc()

        await asyncio.sleep(60)

# =============================================================================
# STARTUP — Single consolidated event
# =============================================================================

@app.on_event("startup")
async def startup():
    """Initialize database, create indexes, and start background tasks."""
    try:
        await ensure_default_tenant()

        # Create indexes for multi-tenant queries
        await db.tenants.create_index("slug", unique=True)
        await db.tenants.create_index("tenant_id", unique=True)
        await db.appointments.create_index([("tenant_id", 1), ("date", 1), ("status", 1)])
        await db.appointments.create_index([("tenant_id", 1), ("id", 1)], unique=True, sparse=True)

        # Prevent double-booking race condition with unique partial index
        await db.appointments.create_index(
            [("tenant_id", 1), ("date", 1), ("time", 1)],
            unique=True,
            partialFilterExpression={"status": {"$in": ["confirmed", "pending_payment"]}},
            name="unique_active_slot"
        )

        # Booking holds TTL index (auto-delete expired holds)
        await db.booking_holds.create_index("expires_at", expireAfterSeconds=0)
        try:
            await db.booking_holds.drop_index("tenant_id_1_date_1")
        except Exception:
            pass
        await db.booking_holds.create_index(
            [("tenant_id", 1), ("date", 1), ("schedule", 1)],
            unique=True
        )

        # Additional query pattern indexes
        await db.appointments.create_index("phone")
        await db.calendar_events.create_index("appointment_id")
        await db.notifications.create_index([("tenant_id", 1), ("is_read", 1), ("created_at", -1)])

    except Exception as e:
        print(f"Warning: Database initialization issue: {e}")

    # Start background expiration monitor
    asyncio.create_task(run_expiration_monitor())

    print("🚀 Gratia Nail Art API started")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
