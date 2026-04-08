"""
Admin conversation analytics — session list, turn details, aggregate stats.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from collections import Counter
from fastapi import APIRouter, Depends, HTTPException

from database import db
from auth import get_current_admin

router = APIRouter(tags=["admin-conversations"])


@router.get("/conversations")
async def get_conversations(
    limit: int = 50,
    session_id: Optional[str] = None,
    admin: dict = Depends(get_current_admin),
):
    """
    Get conversation sessions or turns for a specific session.
    Without session_id: returns session summaries.
    With session_id: returns all turns for that session.
    """
    try:
        if session_id:
            turns = await db.ai_chat_history.find(
                {"session_id": session_id}
            ).sort("timestamp", 1).to_list(length=200)

            return {
                "session_id": session_id,
                "turns": [
                    {
                        "user_message": t.get("user_message", ""),
                        "bot_response": t.get("bot_response", ""),
                        "intent": t.get("intent", ""),
                        "entities": t.get("entities", {}),
                        "tool_name": t.get("tool_name", ""),
                        "frontend_action": t.get("frontend_action"),
                        "timestamp": t.get("timestamp", ""),
                    }
                    for t in turns
                ],
                "total_turns": len(turns),
            }

        sessions = await db.conversation_sessions.find({}).sort(
            "last_message_at", -1
        ).limit(limit).to_list(length=limit)

        return {
            "sessions": [
                {
                    "session_id": s.get("session_id", ""),
                    "started_at": s.get("started_at", ""),
                    "last_message_at": s.get("last_message_at", ""),
                    "turn_count": s.get("turn_count", 0),
                    "intents_used": s.get("intents_used", []),
                    "tools_used": s.get("tools_used", []),
                    "last_intent": s.get("last_intent", ""),
                }
                for s in sessions
            ],
            "total": len(sessions),
        }

    except Exception as e:
        print(f"❌ Conversations error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/stats")
async def get_conversation_stats(admin: dict = Depends(get_current_admin)):
    """Get aggregate stats about PopBot conversations."""
    try:
        now = datetime.now(timezone.utc)
        thirty_days_ago = (now - timedelta(days=30)).isoformat()

        recent_turns = await db.ai_chat_history.find(
            {"timestamp": {"$gte": thirty_days_ago}}
        ).to_list(length=5000)

        recent_sessions = await db.conversation_sessions.find(
            {"started_at": {"$gte": thirty_days_ago}}
        ).to_list(length=1000)

        intent_counts = Counter(
            t.get("intent", "unknown") for t in recent_turns if t.get("intent")
        )

        tool_counts = Counter(
            t.get("tool_name", "") for t in recent_turns if t.get("tool_name")
        )

        booking_sessions = sum(
            1 for s in recent_sessions
            if "book" in s.get("intents_used", []) or "booking_continue" in s.get("intents_used", [])
        )

        payment_sessions = sum(
            1 for t in recent_turns if t.get("frontend_action")
        )

        total_sessions = len(recent_sessions)
        total_turns = sum(s.get("turn_count", 0) for s in recent_sessions)
        avg_turns = round(total_turns / total_sessions, 1) if total_sessions else 0

        return {
            "period": "last_30_days",
            "total_sessions": total_sessions,
            "total_turns": len(recent_turns),
            "avg_turns_per_session": avg_turns,
            "booking_sessions": booking_sessions,
            "payment_opened": payment_sessions,
            "conversion_rate": round(
                (booking_sessions / total_sessions * 100) if total_sessions else 0, 1
            ),
            "intent_distribution": [
                {"intent": intent, "count": count}
                for intent, count in intent_counts.most_common(10)
            ],
            "tool_usage": [
                {"tool": tool, "count": count}
                for tool, count in tool_counts.most_common()
            ],
        }

    except Exception as e:
        print(f"❌ Conversation stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
