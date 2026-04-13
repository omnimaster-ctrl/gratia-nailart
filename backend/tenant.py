"""
Tenant configuration for Gratia Nail Art.
Constants, default tenant data, and tenant lookup functions.
"""

import os
from datetime import datetime, timezone
from database import db


DEFAULT_TENANT_ID = os.environ.get("DEFAULT_TENANT_ID", "660e8400-e29b-41d4-a716-446655440001")
DEFAULT_TENANT_SLUG = os.environ.get("DEFAULT_TENANT_SLUG", "gratianailart")

GRATIA_NAILART_TENANT = {
    "tenant_id": DEFAULT_TENANT_ID,
    "slug": DEFAULT_TENANT_SLUG,
    "status": "active",
    "subscription_tier": "basic",
    "branding": {
        "business_name": "Gratia Nail Art",
        "tagline": "Uñas & Nail Art — Técnicas mixtas",
        "logo_url": "/assets/fairy/fairy_gratia_nobg.png",
        "theme": {
            "primary_color": "#515942",
            "secondary_color": "#cda255",
            "background_color": "#2a2e25"
        }
    },
    "contact": {
        "email": "gratia.nailart@gmail.com",
        "phone": "+52 443 000 0000",
        "instagram_handle": "gratia.nailart"
    },
    "services": [
        {
            "id": "svc-001",
            "name": "Técnica Mixta",
            "description": "Combinación de técnicas para un resultado único y personalizado",
            "duration_minutes": 180,
            "base_price": 500.00,
            "currency": "MXN",
            "is_active": True
        },
        {
            "id": "svc-002",
            "name": "Nail Art Completo",
            "description": "Diseño artístico completo con las técnicas más avanzadas",
            "duration_minutes": 240,
            "base_price": 700.00,
            "currency": "MXN",
            "is_active": True
        },
        {
            "id": "svc-003",
            "name": "Retoque / Mantenimiento",
            "description": "Mantenimiento y retoque de tu diseño para mantenerlo impecable",
            "duration_minutes": 120,
            "base_price": 400.00,
            "currency": "MXN",
            "is_active": True
        }
    ],
    "schedule": {
        "timezone": "America/Mexico_City",
        "slots_per_day": 2,
        "min_advance_hours": 48,
        "max_advance_days": 30,
        "working_days": [0, 1, 2, 3, 4, 5],  # Mon-Sat
        "time_blocks": [
            {"name": "Mañana", "display": "Mañana (9:00 AM - 1:00 PM)", "start": "09:00", "end": "13:00"},
            {"name": "Tarde", "display": "Tarde (4:00 PM - 7:00 PM)", "start": "16:00", "end": "19:00"}
        ]
    },
    "payment": {
        "deposit_amount": 250.00,
        "deposit_currency": "MXN",
        "mercadopago": {
            "connected": True,
            "access_token": None,
            "public_key": os.environ.get('MP_PUBLIC_KEY', ''),
            "use_global_token": True
        }
    },
    "policies": {
        "cancellation": "Se requiere un anticipo de $250 MXN para confirmar tu cita. Si necesitas cancelar, hazlo con al menos 24 horas de anticipación.",
        "max_reschedules": 1
    }
}


async def ensure_default_tenant():
    """Ensure the default Gratia Nail Art tenant exists in the database."""
    existing = await db.tenants.find_one({"tenant_id": DEFAULT_TENANT_ID})
    if not existing:
        tenant_doc = {**GRATIA_NAILART_TENANT, "created_at": datetime.now(timezone.utc).isoformat()}
        await db.tenants.insert_one(tenant_doc)
        print(f"Created default tenant: {DEFAULT_TENANT_SLUG}")
    return existing or GRATIA_NAILART_TENANT


async def get_tenant_by_slug(slug: str):
    """Get tenant configuration by slug."""
    tenant = await db.tenants.find_one({"slug": slug, "status": "active"})
    return tenant


async def get_tenant_by_id(tenant_id: str):
    """Get tenant configuration by ID."""
    tenant = await db.tenants.find_one({"tenant_id": tenant_id, "status": "active"})
    return tenant
