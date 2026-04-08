"""
Admin route modules for La Pop Nails.
Combines all admin sub-routers into a single router for server.py.
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .appointments import router as appointments_router
from .analytics import router as analytics_router
from .clients import router as clients_router
from .blocked_dates import router as blocked_dates_router
from .settings import router as settings_router
from .notifications import router as notifications_router
from .conversations import router as conversations_router
from .setup import router as setup_router

router = APIRouter(prefix="/api/admin")

router.include_router(auth_router)
router.include_router(appointments_router)
router.include_router(analytics_router)
router.include_router(clients_router)
router.include_router(blocked_dates_router)
router.include_router(settings_router)
router.include_router(notifications_router)
router.include_router(conversations_router)
router.include_router(setup_router)
