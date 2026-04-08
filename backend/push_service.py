"""
Web Push notification service using VAPID.
Sends browser push notifications to all registered admin subscriptions.
"""

import json
import os
import traceback

from pywebpush import webpush, WebPushException

from database import db

VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY", "")
VAPID_PUBLIC_KEY = os.environ.get("VAPID_PUBLIC_KEY", "")
VAPID_CLAIMS_EMAIL = os.environ.get("VAPID_CLAIMS_EMAIL", "mailto:lapopnails.28@gmail.com")


async def send_push_to_all(title: str, body: str, url: str = "/admin"):
    """Send push notification to all active admin subscriptions.

    Best-effort delivery — never raises, never blocks the booking flow.
    Expired subscriptions (410 Gone) are automatically cleaned up.
    """
    if not VAPID_PRIVATE_KEY or not VAPID_PUBLIC_KEY:
        print("⚠️ VAPID keys not configured — skipping push notifications")
        return

    payload = json.dumps({"title": title, "body": body, "url": url})
    vapid_claims = {"sub": VAPID_CLAIMS_EMAIL}

    subscriptions = await db.push_subscriptions.find().to_list(length=100)

    for sub_doc in subscriptions:
        subscription_info = sub_doc.get("subscription")
        if not subscription_info:
            continue

        try:
            webpush(
                subscription_info=subscription_info,
                data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=vapid_claims,
            )
        except WebPushException as e:
            if e.response and e.response.status_code == 410:
                # Subscription expired — remove it
                await db.push_subscriptions.delete_one({"_id": sub_doc["_id"]})
                print(f"🗑️ Removed expired push subscription: {subscription_info.get('endpoint', '')[:60]}...")
            else:
                print(f"⚠️ Push failed: {e}")
        except Exception:
            print(f"⚠️ Push error: {traceback.format_exc()}")
