"""
Multi-tenant configuration for La Pop Nails.
Constants, default tenant data, and tenant lookup functions.
"""

import os
from datetime import datetime, timezone
from database import db


DEFAULT_TENANT_ID = os.environ.get("DEFAULT_TENANT_ID", "550e8400-e29b-41d4-a716-446655440000")
DEFAULT_TENANT_SLUG = os.environ.get("DEFAULT_TENANT_SLUG", "lapopnails")

LA_POP_NAILS_TENANT = {
    "tenant_id": DEFAULT_TENANT_ID,
    "slug": DEFAULT_TENANT_SLUG,
    "status": "active",
    "subscription_tier": "premium",
    "branding": {
        "business_name": "La Pop Nails",
        "tagline": "Te espero para crear magia en tus uñas",
        "logo_url": "https://customer-assets.emergentagent.com/job_beauty-hands/artifacts/pvh2nejj_IMG_0010.png",
        "theme": {
            "primary_color": "#ec4899",
            "secondary_color": "#f43f5e",
            "background_color": "#fdf2f8"
        }
    },
    "contact": {
        "email": "lapopnails.28@gmail.com",
        "phone": "+52 123 456 7890",
        "instagram_handle": "___lapopnails"
    },
    "services": [
        {
            "id": "svc-001",
            "name": "Manicura",
            "description": "Mi especialidad es la manicura rusa, una técnica que va mucho más allá de lo tradicional",
            "duration_minutes": 75,
            "base_price": 450.00,
            "currency": "MXN",
            "is_active": True
        },
        {
            "id": "svc-002",
            "name": "Nivelación en uña natural",
            "description": "Esta es una de mis técnicas favoritas porque logra resultados increíbles manteniendo la belleza natural",
            "duration_minutes": 180,
            "base_price": 550.00,
            "currency": "MXN",
            "is_active": True
        },
        {
            "id": "svc-003",
            "name": "Refuerzo en técnica híbrida",
            "description": "Esta técnica es perfecta para mis clientas que tienen uñas frágiles",
            "duration_minutes": 120,
            "base_price": 550.00,
            "currency": "MXN",
            "is_active": True
        },
        {
            "id": "svc-004",
            "name": "Extensión híbrida escultural",
            "description": "Si sueñas con uñas más largas, esta técnica es mi propuesta más artística",
            "duration_minutes": 210,
            "base_price": 650.00,
            "currency": "MXN",
            "is_active": True
        }
    ],
    "schedule": {
        "timezone": "America/Mexico_City",
        "slots_per_day": 2,
        "min_advance_hours": 48,
        "max_advance_days": 30,
        "working_days": [0, 1, 2, 3, 4],
        "time_blocks": [
            {"name": "Mañana", "display": "Mañana (9:00 AM - 12:00 PM)", "start": "09:00", "end": "12:00"},
            {"name": "Tarde", "display": "Tarde (4:00 PM - 7:00 PM)", "start": "16:00", "end": "19:00"}
        ]
    },
    "payment": {
        "deposit_amount": 250.00,
        "deposit_currency": "MXN",
        "mercadopago": {
            "connected": True,
            "access_token": None,
            "public_key": os.environ.get('MP_PUBLIC_KEY', 'APP_USR-3738a2c8-12c9-4410-b855-92f9920cc42f'),
            "use_global_token": True
        }
    },
    "policies": {
        "cancellation": "Se requiere un anticipo de $250 MXN para confirmar tu cita. Si necesitas cancelar, hazlo con al menos 24 horas de anticipación.",
        "max_reschedules": 1
    }
}


async def ensure_default_tenant():
    """Ensure the default La Pop Nails tenant exists in the database."""
    existing = await db.tenants.find_one({"tenant_id": DEFAULT_TENANT_ID})
    if not existing:
        tenant_doc = {**LA_POP_NAILS_TENANT, "created_at": datetime.now(timezone.utc).isoformat()}
        await db.tenants.insert_one(tenant_doc)
        print(f"Created default tenant: {DEFAULT_TENANT_SLUG}")
    return existing or LA_POP_NAILS_TENANT


async def get_tenant_by_slug(slug: str):
    """Get tenant configuration by slug."""
    tenant = await db.tenants.find_one({"slug": slug, "status": "active"})
    return tenant


async def get_tenant_by_id(tenant_id: str):
    """Get tenant configuration by ID."""
    tenant = await db.tenants.find_one({"tenant_id": tenant_id, "status": "active"})
    return tenant
