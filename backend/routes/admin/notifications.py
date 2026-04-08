"""
Admin notifications — unread count, list, mark as read, push subscriptions.
"""

import os
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from database import db
from auth import get_current_admin
from tenant import DEFAULT_TENANT_ID
from models import MarkReadRequest


class PushSubscriptionRequest(BaseModel):
    endpoint: str
    keys: dict  # { p256dh: str, auth: str }

router = APIRouter(tags=["admin-notifications"])


@router.get("/notifications/unread-count")
async def get_unread_count(admin: dict = Depends(get_current_admin)):
    """Get count of unread notifications."""
    try:
        count = await db.notifications.count_documents({
            "tenant_id": DEFAULT_TENANT_ID,
            "is_read": False,
        })
        return {"count": count}
    except Exception as e:
        print(f"❌ Unread count error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/notifications")
async def get_notifications(limit: int = 20, admin: dict = Depends(get_current_admin)):
    """Get latest notifications."""
    try:
        cursor = db.notifications.find(
            {"tenant_id": DEFAULT_TENANT_ID}
        ).sort("created_at", -1).limit(limit)

        notifications = []
        async for doc in cursor:
            notifications.append({
                "id": str(doc["_id"]),
                "type": doc.get("type", ""),
                "title": doc.get("title", ""),
                "body": doc.get("body", ""),
                "appointment_id": doc.get("appointment_id", ""),
                "is_read": doc.get("is_read", False),
                "created_at": doc.get("created_at", ""),
            })

        return {"notifications": notifications}
    except Exception as e:
        print(f"❌ Get notifications error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/notifications/mark-read")
async def mark_notifications_read(
    body: MarkReadRequest,
    admin: dict = Depends(get_current_admin),
):
    """Mark notifications as read."""
    try:
        from bson import ObjectId

        if body.all:
            result = await db.notifications.update_many(
                {"tenant_id": DEFAULT_TENANT_ID, "is_read": False},
                {"$set": {"is_read": True}},
            )
        elif body.ids:
            obj_ids = [ObjectId(id_str) for id_str in body.ids]
            result = await db.notifications.update_many(
                {"_id": {"$in": obj_ids}, "tenant_id": DEFAULT_TENANT_ID},
                {"$set": {"is_read": True}},
            )
        else:
            return {"modified": 0}

        return {"modified": result.modified_count}
    except Exception as e:
        print(f"❌ Mark read error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- Push subscription endpoints ---


@router.get("/push-config")
async def get_push_config(admin: dict = Depends(get_current_admin)):
    """Return VAPID public key so the frontend can subscribe."""
    key = os.environ.get("VAPID_PUBLIC_KEY", "")
    if not key:
        raise HTTPException(status_code=503, detail="Push notifications not configured")
    return {"vapid_public_key": key}


@router.post("/push-subscriptions")
async def save_push_subscription(
    body: PushSubscriptionRequest,
    admin: dict = Depends(get_current_admin),
):
    """Save a browser push subscription."""
    subscription_info = {
        "endpoint": body.endpoint,
        "keys": body.keys,
    }

    # Upsert by endpoint to avoid duplicates
    await db.push_subscriptions.update_one(
        {"subscription.endpoint": body.endpoint},
        {"$set": {
            "subscription": subscription_info,
            "admin_id": admin.get("email", ""),
            "tenant_id": DEFAULT_TENANT_ID,
        }},
        upsert=True,
    )

    return {"status": "subscribed"}


@router.delete("/push-subscriptions")
async def delete_push_subscription(
    body: PushSubscriptionRequest,
    admin: dict = Depends(get_current_admin),
):
    """Remove a browser push subscription."""
    result = await db.push_subscriptions.delete_one(
        {"subscription.endpoint": body.endpoint}
    )
    return {"deleted": result.deleted_count}
