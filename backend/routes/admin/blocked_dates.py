"""
Admin blocked dates management — vacations, holidays, personal days.
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status

from database import db
from auth import get_current_admin
from tenant import DEFAULT_TENANT_ID
from models import BlockedDateRequest

router = APIRouter(tags=["admin-blocked-dates"])


@router.post("/blocked-dates")
async def create_blocked_date(
    blocked_date: BlockedDateRequest,
    admin: dict = Depends(get_current_admin)
):
    """Block a date so it's unavailable for client bookings."""
    try:
        try:
            datetime.strptime(blocked_date.date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )

        existing = await db.blocked_dates.find_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": blocked_date.date
        })

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta fecha ya está bloqueada"
            )

        blocked_doc = {
            "tenant_id": DEFAULT_TENANT_ID,
            "date": blocked_date.date,
            "reason": blocked_date.reason,
            "all_day": blocked_date.all_day,
            "created_by": admin["email"],
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        result = await db.blocked_dates.insert_one(blocked_doc)

        await db.blocked_dates.create_index([("tenant_id", 1), ("date", 1)], unique=True)

        return {
            "success": True,
            "message": f"Fecha bloqueada: {blocked_date.date}",
            "blocked_date": {
                "id": str(result.inserted_id),
                "date": blocked_date.date,
                "reason": blocked_date.reason
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error blocking date: {e}")
        raise HTTPException(status_code=500, detail=f"Error al bloquear fecha: {str(e)}")


@router.get("/blocked-dates")
async def get_blocked_dates(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    admin: dict = Depends(get_current_admin)
):
    """Get all blocked dates, optionally filtered by date range."""
    try:
        query_filter = {"tenant_id": DEFAULT_TENANT_ID}

        if start_date or end_date:
            date_filter = {}
            if start_date:
                date_filter["$gte"] = start_date
            if end_date:
                date_filter["$lte"] = end_date

            if date_filter:
                query_filter["date"] = date_filter

        blocked_dates = await db.blocked_dates.find(query_filter).sort("date", 1).to_list(length=1000)

        formatted_dates = [
            {
                "id": str(bd["_id"]),
                "date": bd.get("date"),
                "reason": bd.get("reason", "Fecha bloqueada"),
                "all_day": bd.get("all_day", True),
                "created_by": bd.get("created_by"),
                "created_at": bd.get("created_at")
            }
            for bd in blocked_dates
        ]

        return {
            "success": True,
            "blocked_dates": formatted_dates,
            "total": len(formatted_dates)
        }

    except Exception as e:
        print(f"❌ Error fetching blocked dates: {e}")
        raise HTTPException(status_code=500, detail=f"Error al obtener fechas bloqueadas: {str(e)}")


@router.delete("/blocked-dates/{date}")
async def delete_blocked_date(
    date: str,
    admin: dict = Depends(get_current_admin)
):
    """Unblock a date, making it available for bookings again."""
    try:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )

        result = await db.blocked_dates.delete_one({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": date
        })

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fecha bloqueada no encontrada"
            )

        return {
            "success": True,
            "message": f"Fecha desbloqueada: {date}",
            "date": date
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error unblocking date: {e}")
        raise HTTPException(status_code=500, detail=f"Error al desbloquear fecha: {str(e)}")
