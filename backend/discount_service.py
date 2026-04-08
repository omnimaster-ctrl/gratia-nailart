from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

# --- Models ---

class DiscountConstraint(BaseModel):
    min_spend: Optional[float] = None
    min_services_count: Optional[int] = None
    specific_services: Optional[List[str]] = None  # List of Service IDs/Names
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    max_global_uses: Optional[int] = None
    max_user_uses: Optional[int] = None

class DiscountStats(BaseModel):
    redeemed_count: int = 0
    total_saved_amount: float = 0.0

class Discount(BaseModel):
    code: str  # Unique, Uppercase
    type: str  # "PERCENTAGE", "FIXED"
    value: float
    description: Optional[str] = None
    waive_deposit: bool = False  # New VIP field
    constraints: DiscountConstraint = Field(default_factory=DiscountConstraint)
    stats: DiscountStats = Field(default_factory=DiscountStats)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DiscountValidationRequest(BaseModel):
    code: str
    cart_total: float
    service_id: Optional[str] = None
    customer_phone: Optional[str] = None

class DiscountValidationResponse(BaseModel):
    valid: bool
    discount_amount: float
    message: str
    final_total: float
    code: Optional[str] = None
    waive_deposit: bool = False

# --- Service Logic ---

async def validate_discount(
    db: AsyncIOMotorDatabase, 
    request: DiscountValidationRequest
) -> DiscountValidationResponse:
    """Read-only validation of a discount code."""
    code = request.code.upper().strip()
    
    # 1. Fetch Discount
    discount_doc = await db.discounts.find_one({"code": code, "is_active": True})
    
    if not discount_doc:
        return DiscountValidationResponse(
            valid=False, discount_amount=0, message="Cupón inválido o expirado", final_total=request.cart_total
        )
    
    discount = Discount(**discount_doc)
    constraints = discount.constraints
    
    # 2. Validate Constraints
    
    # Date Check
    now = datetime.now(timezone.utc)
    if constraints.start_date and now < constraints.start_date:
        return DiscountValidationResponse(
            valid=False, discount_amount=0, message="Este cupón aún no está activo", final_total=request.cart_total
        )
    if constraints.end_date and now > constraints.end_date:
        return DiscountValidationResponse(
            valid=False, discount_amount=0, message="Este cupón ha expirado", final_total=request.cart_total
        )
        
    # Global Limits
    if constraints.max_global_uses and discount.stats.redeemed_count >= constraints.max_global_uses:
        return DiscountValidationResponse(
            valid=False, discount_amount=0, message="Este cupón se ha agotado", final_total=request.cart_total
        )
        
    # Min Spend
    if constraints.min_spend and request.cart_total < constraints.min_spend:
        return DiscountValidationResponse(
            valid=False, discount_amount=0, 
            message=f"Monto mínimo de compra: ${constraints.min_spend}", 
            final_total=request.cart_total
        )

    # 3. Calculate Discount
    discount_amount = 0
    if discount.type == "PERCENTAGE":
        discount_amount = (request.cart_total * discount.value) / 100
        # Optional: Max discount cap could be added here
    elif discount.type == "FIXED":
        discount_amount = discount.value
    
    # Ensure we don't discount more than the total
    if discount_amount > request.cart_total:
        discount_amount = request.cart_total
        
    final_total = request.cart_total - discount_amount
    
    return DiscountValidationResponse(
        valid=True,
        discount_amount=round(discount_amount, 2),
        final_total=round(final_total, 2),
        message="¡Cupón aplicado con éxito!",
        code=discount.code,
        waive_deposit=discount.waive_deposit
    )

async def redeem_discount_atomic(
    db: AsyncIOMotorDatabase, 
    code: str, 
    saved_amount: float
) -> bool:
    """
    Atomically increments usage count.
    Returns True if successful, False if limit reached (Race condition caught).
    """
    code = code.upper().strip()
    
    # We only increment if redeemed_count < max_global_uses (or if no limit exists)
    # Since MongoDB queries allow complex logic, we can construct the query dynamically.
    
    query = {"code": code, "is_active": True}
    
    # Fetch first to check if max_global_uses exists
    # Optimization: We could just try the update with the condition safely.
    
    discount_doc = await db.discounts.find_one({"code": code})
    if not discount_doc:
        return False
        
    constraints = discount_doc.get('constraints', {})
    max_uses = constraints.get('max_global_uses')
    
    if max_uses is not None:
        query["stats.redeemed_count"] = {"$lt": max_uses}
        
    update_result = await db.discounts.update_one(
        query,
        {
            "$inc": {
                "stats.redeemed_count": 1,
                "stats.total_saved_amount": saved_amount
            }
        }
    )
    
    return update_result.modified_count > 0
