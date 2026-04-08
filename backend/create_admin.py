"""
Setup script to create the first admin user for La Pop Nails
Run this script once to initialize the admin panel
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path to import auth module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from auth import get_password_hash, validate_password_strength
from tenant import DEFAULT_TENANT_ID

load_dotenv()


async def create_admin_user():
    """Create first admin user for La Pop Nails."""
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.lapopnails_db

    print("\n" + "="*60)
    print("🔐 La Pop Nails - Admin User Setup")
    print("="*60 + "\n")

    # Get admin details
    email = input("📧 Admin email: ").strip()
    if not email or '@' not in email:
        print("❌ Email inválido")
        return

    # Check if admin already exists
    existing = await db.admin_users.find_one({"email": email})
    if existing:
        print(f"❌ Admin user {email} already exists")
        return

    full_name = input("👤 Full name: ").strip()
    if not full_name:
        print("❌ Name is required")
        return

    # Get and validate password
    while True:
        password = input("🔑 Password (min 12 chars, with upper, lower, digit, special): ").strip()
        is_valid, error_msg = validate_password_strength(password)

        if is_valid:
            confirm_password = input("🔑 Confirm password: ").strip()
            if password != confirm_password:
                print("❌ Passwords do not match. Try again.\n")
                continue
            break
        else:
            print(f"❌ {error_msg}\n")

    print("\n⏳ Creating admin user...")

    # Create admin user document
    admin_user = {
        "tenant_id": DEFAULT_TENANT_ID,
        "email": email,
        "password_hash": get_password_hash(password),
        "full_name": full_name,
        "role": "owner",
        "is_active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_login_at": None,
        "login_attempts": 0,
        "locked_until": None
    }

    # Insert admin user
    result = await db.admin_users.insert_one(admin_user)

    # Create indexes for performance and uniqueness
    await db.admin_users.create_index(
        [("email", 1), ("tenant_id", 1)],
        unique=True,
        name="email_tenant_unique"
    )
    await db.admin_users.create_index(
        [("tenant_id", 1)],
        name="tenant_index"
    )

    print("\n" + "="*60)
    print("✅ Admin user created successfully!")
    print("="*60)
    print(f"\n📧 Email: {email}")
    print(f"👤 Name: {full_name}")
    print(f"🆔 User ID: {result.inserted_id}")
    print(f"🏢 Tenant ID: {DEFAULT_TENANT_ID}")
    print(f"\n🌐 You can now login at: /admin/login\n")

    client.close()


if __name__ == "__main__":
    asyncio.run(create_admin_user())
