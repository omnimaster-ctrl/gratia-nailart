"""
Discount/coupon routes for La Pop Nails.
Validation, CRUD, and usage logging.
"""

from fastapi import APIRouter, Depends, HTTPException

from database import db
from auth import get_current_admin
from models import FrontendCouponRequest, DiscountUsageLog
from discount_service import (
    validate_discount,
    DiscountValidationRequest,
    Discount,
)

router = APIRouter(prefix="/api", tags=["discounts"])


async def log_discount_usage(db, log: DiscountUsageLog):
    try:
        await db.discount_logs.insert_one(log.dict())
    except Exception as e:
        print(f"⚠️ Failed to log discount usage: {e}")


@router.post("/validate-coupon")
async def validate_coupon_endpoint(request: FrontendCouponRequest):
    """Public endpoint for checking coupons from the Wizard"""
    validation_request = DiscountValidationRequest(
        code=request.coupon_code,
        cart_total=request.service_price,
        service_id=request.service_type
    )

    result = await validate_discount(db, validation_request)

    return {
        "valid": result.valid,
        "discount_amount": result.discount_amount,
        "message": result.message,
        "code": result.code,
        "waive_deposit": result.waive_deposit
    }


@router.post("/admin/discounts")
async def create_discount(discount: Discount, admin=Depends(get_current_admin)):
    """Admin endpoint to create new discounts"""
    existing = await db.discounts.find_one({"code": discount.code})
    if existing:
        raise HTTPException(status_code=400, detail="El código de descuento ya existe")

    await db.discounts.insert_one(discount.dict())
    return {"status": "success", "code": discount.code}


@router.get("/admin/discounts")
async def get_discounts(admin=Depends(get_current_admin)):
    """Fetch all discounts with their live stats"""
    cursor = db.discounts.find({}).sort("created_at", -1)
    discounts = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        discounts.append(doc)
    return discounts


@router.patch("/admin/discounts/{code}/toggle")
async def toggle_discount(code: str, admin=Depends(get_current_admin)):
    """Deactivate/Reactivate a discount code (Soft Delete)"""
    discount = await db.discounts.find_one({"code": code})
    if not discount:
        raise HTTPException(status_code=404, detail="Cupón no encontrado")

    new_status = not discount.get("is_active", True)

    await db.discounts.update_one(
        {"code": code},
        {"$set": {"is_active": new_status}}
    )

    return {"status": "success", "new_state": new_status}


@router.delete("/admin/discounts/{code}")
async def delete_discount(code: str, admin=Depends(get_current_admin)):
    """Permanently delete a discount code"""
    result = await db.discounts.delete_one({"code": code})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cupón no encontrado")
    return {"status": "success", "message": "Cupón eliminado permanentemente"}
