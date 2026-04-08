"""
Admin tenant settings — get and update business configuration.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from database import db
from auth import get_current_admin
from tenant import DEFAULT_TENANT_ID
from models import TenantSettingsUpdate

router = APIRouter(tags=["admin-settings"])


@router.get("/settings")
async def get_tenant_settings(admin: dict = Depends(get_current_admin)):
    """Get tenant settings (one_appointment_per_day, etc.)"""
    try:
        settings = await db.tenant_settings.find_one({
            "tenant_id": DEFAULT_TENANT_ID
        })

        if not settings:
            return {
                "one_appointment_per_day": False,
                "retiro_material_price": 150,
                "anticipo_amount": 250
            }

        return {
            "one_appointment_per_day": settings.get("one_appointment_per_day", False),
            "retiro_material_price": settings.get("retiro_material_price", 150),
            "anticipo_amount": settings.get("anticipo_amount", 250)
        }

    except Exception as e:
        print(f"❌ Get settings error: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving settings: {str(e)}")


@router.put("/settings")
async def update_tenant_settings(
    settings_update: TenantSettingsUpdate,
    admin: dict = Depends(get_current_admin)
):
    """Update tenant settings."""
    try:
        update_doc = {
            "tenant_id": DEFAULT_TENANT_ID,
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "updated_by": admin["email"]
        }

        if settings_update.one_appointment_per_day is not None:
            update_doc["one_appointment_per_day"] = settings_update.one_appointment_per_day

        if settings_update.retiro_material_price is not None:
            update_doc["retiro_material_price"] = settings_update.retiro_material_price

        if settings_update.anticipo_amount is not None:
            update_doc["anticipo_amount"] = settings_update.anticipo_amount

        await db.tenant_settings.update_one(
            {"tenant_id": DEFAULT_TENANT_ID},
            {"$set": update_doc},
            upsert=True
        )

        print(f"✅ Settings updated by {admin['email']}: {update_doc}")

        updated = await db.tenant_settings.find_one({"tenant_id": DEFAULT_TENANT_ID})

        return {
            "success": True,
            "message": "Settings updated successfully",
            "settings": {
                "one_appointment_per_day": updated.get("one_appointment_per_day", False),
                "retiro_material_price": updated.get("retiro_material_price", 150),
                "anticipo_amount": updated.get("anticipo_amount", 250)
            }
        }

    except Exception as e:
        print(f"❌ Update settings error: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating settings: {str(e)}")
