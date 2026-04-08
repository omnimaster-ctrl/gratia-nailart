"""Langfuse observability for PopBot.

Provides a callback handler for LangGraph tracing.
Gracefully degrades if Langfuse is not configured.
"""

import os

_langfuse_available = False

try:
    from langfuse.langchain import CallbackHandler
    _langfuse_available = True
except ImportError:
    CallbackHandler = None


def get_langfuse_handler(session_id: str = "", user_id: str = ""):
    """Create a Langfuse callback handler for a single request.

    Returns None if Langfuse is not configured, so callers can
    safely skip it without branching.
    """
    if not _langfuse_available:
        return None

    if not os.environ.get("LANGFUSE_SECRET_KEY"):
        return None

    try:
        metadata = {}
        if session_id:
            metadata["langfuse_session_id"] = session_id
        if user_id:
            metadata["langfuse_user_id"] = user_id

        handler = CallbackHandler(
            session_id=session_id or None,
            user_id=user_id or None,
            tags=["popbot", "production"],
        )
        return handler
    except Exception as e:
        print(f"[PopBot] Langfuse handler init failed: {e}")
        return None
