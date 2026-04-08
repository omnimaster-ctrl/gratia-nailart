"""
Admin authentication routes — login, session, logout.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status

from auth import (
    authenticate_admin,
    create_access_token,
    get_current_admin,
    update_login_attempt,
    is_account_locked,
    ACCESS_TOKEN_EXPIRE_HOURS,
)
from models import LoginRequest, LoginResponse, AdminResponse

router = APIRouter(tags=["admin-auth"])


@router.post("/login", response_model=LoginResponse)
async def admin_login(login_data: LoginRequest):
    """Authenticate admin user and return JWT access token."""
    if await is_account_locked(login_data.email):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta bloqueada por múltiples intentos fallidos. Intenta en 15 minutos."
        )

    admin = await authenticate_admin(login_data.email, login_data.password)

    if not admin:
        await update_login_attempt(login_data.email, success=False)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await update_login_attempt(login_data.email, success=True)

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={
            "sub": str(admin["_id"]),
            "email": admin["email"],
            "role": admin["role"],
            "tenant_id": admin["tenant_id"]
        },
        expires_delta=access_token_expires
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        admin={
            "email": admin["email"],
            "full_name": admin["full_name"],
            "role": admin["role"],
            "tenant_id": admin["tenant_id"]
        }
    )


@router.get("/me", response_model=AdminResponse)
async def get_current_admin_user(admin: dict = Depends(get_current_admin)):
    """Get current authenticated admin user information."""
    return AdminResponse(
        email=admin["email"],
        full_name=admin["full_name"],
        role=admin["role"],
        tenant_id=admin["tenant_id"]
    )


@router.post("/logout")
async def admin_logout(admin: dict = Depends(get_current_admin)):
    """Logout admin user (stateless — client removes token)."""
    return {
        "message": "Sesión cerrada exitosamente",
        "email": admin["email"]
    }
