"""
Unified notification service.
Inserts an in-app notification AND triggers push to all subscribers.
"""

from datetime import datetime, timezone

from database import db
from push_service import send_push_to_all
from tenant import DEFAULT_TENANT_ID


async def create_notification(
    type: str,
    title: str,
    body: str,
    appointment_id: str = None,
):
    """Insert a notification document and send push to all admin subscribers."""
    doc = {
        "tenant_id": DEFAULT_TENANT_ID,
        "type": type,
        "title": title,
        "body": body,
        "is_read": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    if appointment_id:
        doc["appointment_id"] = appointment_id

    await db.notifications.insert_one(doc)
    await send_push_to_all(title=title, body=body, url="/admin")
