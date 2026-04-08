"""
Authentication module for La Pop Nails Admin Panel
Provides JWT token generation, validation, and password hashing
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
import hmac
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from database import db
from tenant import DEFAULT_TENANT_ID

load_dotenv()

# Internal machine-to-machine token (for agent/bot API calls)
INTERNAL_API_TOKEN = os.environ.get("INTERNAL_API_TOKEN")


async def verify_internal_token(request: Request):
    """Validate X-Internal-Token header for machine-to-machine calls."""
    token = request.headers.get("X-Internal-Token")
    if not INTERNAL_API_TOKEN or not token or not hmac.compare_digest(token, INTERNAL_API_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid internal token")
    return True


# JWT Configuration
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is required. Set it before starting the server.")
ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_HOURS = int(os.environ.get('JWT_EXPIRE_HOURS', '24'))

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer security scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The password provided by the user
        hashed_password: The hashed password from the database

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing in the database.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing token payload (sub, email, role, etc.)
        expires_delta: Optional custom expiration time

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_admin_user_by_email(email: str):
    """
    Retrieve admin user from database by email.

    Args:
        email: Admin user's email address

    Returns:
        dict: Admin user document or None if not found
    """
    admin_user = await db.admin_users.find_one({
        "email": email,
        "tenant_id": DEFAULT_TENANT_ID
    })
    return admin_user


async def authenticate_admin(email: str, password: str):
    """
    Authenticate an admin user with email and password.

    Args:
        email: Admin user's email
        password: Plain text password

    Returns:
        dict: Admin user document if authenticated, None otherwise
    """
    admin = await get_admin_user_by_email(email)

    if not admin:
        return None

    if not admin.get('is_active', True):
        return None

    if not verify_password(password, admin['password_hash']):
        return None

    return admin


async def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to get the current authenticated admin user from JWT token.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        dict: Current admin user document

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    admin = await get_admin_user_by_email(email)

    if admin is None:
        raise credentials_exception

    if not admin.get('is_active', True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado"
        )

    return admin


async def update_login_attempt(email: str, success: bool):
    """
    Update login attempt count and lock status.

    Args:
        email: Admin user's email
        success: Whether the login was successful
    """
    admin = await get_admin_user_by_email(email)

    if not admin:
        return

    if success:
        # Reset login attempts on successful login
        await db.admin_users.update_one(
            {"email": email, "tenant_id": DEFAULT_TENANT_ID},
            {
                "$set": {
                    "login_attempts": 0,
                    "locked_until": None,
                    "last_login_at": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    else:
        # Increment login attempts
        login_attempts = admin.get('login_attempts', 0) + 1
        update_data = {"login_attempts": login_attempts}

        # Lock account after 5 failed attempts for 15 minutes
        if login_attempts >= 5:
            locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            update_data["locked_until"] = locked_until.isoformat()

        await db.admin_users.update_one(
            {"email": email, "tenant_id": DEFAULT_TENANT_ID},
            {"$set": update_data}
        )


async def is_account_locked(email: str) -> bool:
    """
    Check if an account is currently locked.

    Args:
        email: Admin user's email

    Returns:
        bool: True if account is locked, False otherwise
    """
    admin = await get_admin_user_by_email(email)

    if not admin:
        return False

    locked_until_str = admin.get('locked_until')

    if not locked_until_str:
        return False

    locked_until = datetime.fromisoformat(locked_until_str)

    if datetime.now(timezone.utc) < locked_until:
        return True

    # Lock period expired, reset
    await db.admin_users.update_one(
        {"email": email, "tenant_id": DEFAULT_TENANT_ID},
        {"$set": {"locked_until": None, "login_attempts": 0}}
    )

    return False


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets security requirements.

    Args:
        password: Password to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if len(password) < 12:
        return False, "La contraseña debe tener al menos 12 caracteres"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '@$!%*?&#' for c in password)

    if not (has_upper and has_lower and has_digit and has_special):
        return False, "La contraseña debe contener mayúsculas, minúsculas, números y caracteres especiales (@$!%*?&#)"

    return True, ""
