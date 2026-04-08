"""
Admin setup — first admin creation, database stats, cleanup.
"""

from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status

from database import db
from auth import get_current_admin
from tenant import DEFAULT_TENANT_ID
from models import SetupAdminRequest

router = APIRouter(tags=["admin-setup"])


@router.post("/setup-first-admin")
async def setup_first_admin(admin_data: SetupAdminRequest):
    """One-time setup endpoint to create the first admin user."""
    from auth import get_password_hash, validate_password_strength

    existing_admins = await db.admin_users.count_documents({})
    if existing_admins > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin users already exist. Use the admin panel to create additional admins."
        )

    is_valid, message = validate_password_strength(admin_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    admin_user = {
        "tenant_id": DEFAULT_TENANT_ID,
        "email": admin_data.email.lower(),
        "password_hash": get_password_hash(admin_data.password),
        "full_name": admin_data.full_name,
        "role": "owner",
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_login_at": None,
        "login_attempts": 0,
        "locked_until": None
    }

    try:
        result = await db.admin_users.insert_one(admin_user)

        await db.admin_users.create_index(
            [("email", 1), ("tenant_id", 1)],
            unique=True
        )

        return {
            "success": True,
            "message": "First admin user created successfully",
            "email": admin_data.email,
            "full_name": admin_data.full_name
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create admin user: {str(e)}"
        )


@router.get("/database-stats")
async def get_database_stats(admin: dict = Depends(get_current_admin)):
    """Check database collection sizes and document counts."""
    stats = {}

    collection_names = await db.list_collection_names()

    for collection_name in collection_names:
        collection = db[collection_name]
        count = await collection.count_documents({})
        stats[collection_name] = {
            "document_count": count
        }

    return {
        "database": db.name,
        "collections": stats,
        "total_collections": len(collection_names)
    }


@router.delete("/cleanup-database")
async def cleanup_database(admin: dict = Depends(get_current_admin)):
    """Emergency cleanup: Delete old test data and appointments."""
    deleted_stats = {}

    ninety_days_ago = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()

    appointments_result = await db.appointments.delete_many({
        "date": {"$lt": ninety_days_ago.split("T")[0]}
    })
    deleted_stats["old_appointments"] = appointments_result.deleted_count

    cancelled_result = await db.appointments.delete_many({
        "status": "cancelled"
    })
    deleted_stats["cancelled_appointments"] = cancelled_result.deleted_count

    return {
        "success": True,
        "deleted": deleted_stats,
        "message": "Database cleanup completed"
    }
