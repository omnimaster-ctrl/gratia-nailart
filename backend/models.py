"""
Pydantic request/response models for La Pop Nails API.
Shared across all route modules.
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List


class AppointmentRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    currentNailsImages: Optional[List[dict]] = Field(default=[])
    service: str = Field(..., min_length=3, max_length=100)
    retiro: bool = Field(default=False)
    tieneIdeas: bool = Field(default=False)
    imagenes: Optional[List[dict]] = Field(default=[])
    libertadArtistica: bool = Field(default=False)
    date: str = Field(..., description="YYYY-MM-DD format")
    schedule: str = Field(..., description="Schedule time range")
    time: str = Field(..., description="HH:MM format")
    notes: Optional[str] = Field(None, max_length=500)
    aceptaPoliticas: bool = Field(..., description="Must accept policies")
    favoriteSnacks: Optional[str] = Field(None, max_length=200)
    favoriteDrinks: Optional[str] = Field(None, max_length=200)
    favoriteMovie: Optional[str] = Field(None, max_length=200)
    favoriteSeries: Optional[str] = Field(None, max_length=200)
    favoriteMusic: Optional[str] = Field(None, max_length=200)
    birthday: Optional[str] = Field(None, description="MM-DD format")


class AgentBookingRequest(BaseModel):
    """Booking model for agent-created bookings."""
    name: str
    phone: str
    service: str
    date: str      # YYYY-MM-DD
    time: str      # HH:MM
    email: Optional[str] = None
    favoriteSnacks: Optional[str] = None
    favoriteDrinks: Optional[str] = None
    favoriteMovie: Optional[str] = None
    favoriteSeries: Optional[str] = None
    favoriteMusic: Optional[str] = None
    birthday: Optional[str] = None


class PaymentRequest(BaseModel):
    appointment_data: AppointmentRequest
    customer_email: EmailStr


class RescheduleRequest(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)


class RescheduleUpdate(BaseModel):
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    new_date: str = Field(..., description="YYYY-MM-DD format")
    new_schedule: str = Field(..., description="Schedule time range")
    new_time: str = Field(..., description="HH:MM format")


class TokenRescheduleRequest(BaseModel):
    new_date: str = Field(..., description="YYYY-MM-DD format")
    new_schedule: str = Field(..., description="Schedule time range (Mañana/Tarde)")
    new_time: str = Field(..., description="HH:MM format")


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None


class BusinessInfo(BaseModel):
    name: str = "La Pop Nails"
    services: List[str] = [
        "Manicura - Mi especialidad es la manicura rusa, una técnica que va mucho más allá de lo tradicional",
        "Nivelación en uña natural - Esta es una de mis técnicas favoritas porque logra resultados increíbles manteniendo la belleza natural",
        "Refuerzo en técnica híbrida - Esta técnica es perfecta para mis clientas que tienen uñas frágiles",
        "Extensión híbrida escultural - Si sueñas con uñas más largas, esta técnica es mi propuesta más artística"
    ]
    schedule: str = "Lunes a Viernes: 9:00 AM - 12:00 PM y 4:00 PM - 7:00 PM"
    instagram: str = "@___lapopnails"
    contact_method: str = "Instagram Direct Message"


class TestEmailRequest(BaseModel):
    email: str = "tellob.buider10@gmail.com"


class AIChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[dict]] = []


class FrontendCouponRequest(BaseModel):
    coupon_code: str
    service_type: str
    service_price: float


class DiscountUsageLog(BaseModel):
    coupon_code: str
    appointment_id: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    service_id: str
    original_price: float
    discount_amount: float
    final_price: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "redeemed"


class BypassBookingRequest(BaseModel):
    appointment_data: AppointmentRequest
    coupon_code: str
    customer_email: EmailStr


# =============================================================================
# ADMIN MODELS
# =============================================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    admin: dict


class AdminResponse(BaseModel):
    email: str
    full_name: str
    role: str
    tenant_id: str


class TenantSettingsUpdate(BaseModel):
    one_appointment_per_day: Optional[bool] = None
    retiro_material_price: Optional[int] = None
    anticipo_amount: Optional[int] = None


class AdminAppointmentResponse(BaseModel):
    id: str
    date: str
    time: str
    schedule: str
    status: str
    client: dict
    service: str
    service_duration: str
    preferences: Optional[dict] = None
    payment: dict
    created_at: str


class WeeklyAppointmentsResponse(BaseModel):
    week_start: str
    week_end: str
    appointments: List[AdminAppointmentResponse]
    stats: dict


class CancelAppointmentRequest(BaseModel):
    reason: Optional[str] = None
    notify_client: bool = True


class SetupAdminRequest(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class BlockedDateRequest(BaseModel):
    date: str
    reason: Optional[str] = "Fecha bloqueada"
    all_day: bool = True


class UpdateClientRequest(BaseModel):
    notes: Optional[str] = None
    is_vip: Optional[bool] = None


class MarkReadRequest(BaseModel):
    ids: Optional[List[str]] = None
    all: Optional[bool] = False
