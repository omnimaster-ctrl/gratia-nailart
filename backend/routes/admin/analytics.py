"""
Admin analytics — dashboard metrics, revenue, services breakdown.
"""

from datetime import datetime, timedelta, timezone
from collections import Counter
from fastapi import APIRouter, Depends, HTTPException

from database import db
from auth import get_current_admin
from tenant import DEFAULT_TENANT_ID

router = APIRouter(tags=["admin-analytics"])


@router.get("/analytics/dashboard")
async def get_dashboard_analytics(admin: dict = Depends(get_current_admin)):
    """Get analytics dashboard data for admin panel."""
    try:
        now = datetime.now(timezone.utc)
        first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        confirmed_appointments = await db.appointments.find({
            "tenant_id": DEFAULT_TENANT_ID,
            "status": "confirmed",
            "date": {"$gte": first_day_of_month.strftime("%Y-%m-%d")}
        }).to_list(length=1000)

        all_appointments_month = await db.appointments.find({
            "tenant_id": DEFAULT_TENANT_ID,
            "date": {"$gte": first_day_of_month.strftime("%Y-%m-%d")}
        }).to_list(length=1000)

        cancelled_appointments = [apt for apt in all_appointments_month if apt.get("status") == "cancelled"]

        all_clients = await db.clients.find({
            "tenant_id": DEFAULT_TENANT_ID
        }).to_list(length=10000)

        # Monthly Revenue
        monthly_revenue = len(confirmed_appointments) * 250

        # Appointments This Month
        appointments_this_month = len(confirmed_appointments)

        # New Clients This Month
        new_clients_this_month = 0
        for client in all_clients:
            client_created = client.get("created_at", "")
            if client_created and client_created >= first_day_of_month.isoformat():
                new_clients_this_month += 1

        # Most Popular Service
        service_counts = Counter([apt.get("service", "Unknown") for apt in confirmed_appointments])
        most_popular_service = service_counts.most_common(1)[0] if service_counts else ("N/A", 0)

        # Services Chart
        services_data = [
            {"name": service, "count": count, "percentage": round((count / len(confirmed_appointments) * 100) if confirmed_appointments else 0, 1)}
            for service, count in service_counts.most_common()
        ]

        # Upcoming Birthdays (next 30 days)
        upcoming_birthdays = []
        today = now.date()
        for client in all_clients:
            birthday_str = client.get("birthday")
            if birthday_str:
                try:
                    birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
                    this_year_birthday = birthday.replace(year=today.year)
                    next_year_birthday = birthday.replace(year=today.year + 1)

                    days_until = (this_year_birthday - today).days
                    if days_until < 0:
                        days_until = (next_year_birthday - today).days
                        birthday_date = next_year_birthday
                    else:
                        birthday_date = this_year_birthday

                    if 0 <= days_until <= 30:
                        upcoming_birthdays.append({
                            "name": client.get("name", "Cliente"),
                            "phone": client.get("phone", ""),
                            "date": birthday_date.strftime("%Y-%m-%d"),
                            "days_until": days_until
                        })
                except:
                    pass

        upcoming_birthdays.sort(key=lambda x: x["days_until"])

        # Weekly Appointments breakdown
        days_since_monday = now.weekday()
        start_of_week = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)

        weekly_appointments = {}
        days_of_week = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        for i, day_name in enumerate(days_of_week):
            day_date = start_of_week + timedelta(days=i)
            day_str = day_date.strftime("%Y-%m-%d")

            count = sum(1 for apt in all_appointments_month
                       if apt.get("date") == day_str and apt.get("status") == "confirmed")

            weekly_appointments[day_name] = {
                "date": day_str,
                "count": count,
                "is_today": day_date.date() == today
            }

        # Cancellation Metrics
        total_cancelled = len(cancelled_appointments)
        total_bookings = len(all_appointments_month)
        cancellation_rate = round((total_cancelled / total_bookings * 100) if total_bookings > 0 else 0, 1)
        revenue_lost = total_cancelled * 250

        return {
            "success": True,
            "period": {
                "month": now.strftime("%B %Y"),
                "month_start": first_day_of_month.isoformat(),
                "current_date": now.isoformat()
            },
            "metrics": {
                "monthly_revenue": {
                    "value": monthly_revenue,
                    "currency": "MXN",
                    "label": "Ingresos del Mes"
                },
                "appointments_this_month": {
                    "value": appointments_this_month,
                    "label": "Citas Este Mes"
                },
                "new_clients": {
                    "value": new_clients_this_month,
                    "label": "Clientes Nuevos"
                },
                "most_popular_service": {
                    "name": most_popular_service[0],
                    "count": most_popular_service[1],
                    "label": "Servicio Más Popular"
                },
                "cancellations": {
                    "total": total_cancelled,
                    "rate": cancellation_rate,
                    "revenue_lost": revenue_lost,
                    "label": "Cancelaciones"
                }
            },
            "services_chart": services_data,
            "upcoming_birthdays": upcoming_birthdays[:10],
            "weekly_appointments": weekly_appointments
        }

    except Exception as e:
        print(f"❌ Analytics error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")
