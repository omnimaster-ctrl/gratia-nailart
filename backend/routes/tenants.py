"""
Tenant public routes for La Pop Nails.
"""

from fastapi import APIRouter, HTTPException

from tenant import get_tenant_by_slug

router = APIRouter(prefix="/api", tags=["tenants"])


@router.get("/t/{slug}/config")
async def get_tenant_config(slug: str):
    """Get public tenant configuration for customer-facing pages."""
    tenant = await get_tenant_by_slug(slug)

    if not tenant:
        raise HTTPException(status_code=404, detail="Salon not found")

    return {
        "tenant_id": tenant["tenant_id"],
        "slug": tenant["slug"],
        "branding": tenant["branding"],
        "contact": tenant["contact"],
        "services": [s for s in tenant["services"] if s.get("is_active", True)],
        "schedule": tenant["schedule"],
        "payment": {
            "deposit_amount": tenant["payment"]["deposit_amount"],
            "deposit_currency": tenant["payment"]["deposit_currency"],
            "mercadopago_public_key": tenant["payment"]["mercadopago"].get("public_key"),
            "connected": tenant["payment"]["mercadopago"].get("connected", False)
        },
        "policies": tenant.get("policies", {})
    }
