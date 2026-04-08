
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def inspect():
    try:
        MONGO_URL = os.environ.get('MONGO_URL')
        if not MONGO_URL:
            print("❌ MONGO_URL not found")
            return

        client = AsyncIOMotorClient(MONGO_URL)
        db = client.lapopnails_db
        
        email = "kaipahola@gmail.com"
        print(f"\n🔍 Searching for appointments with email: {email}")
        
        # 1. Search in Appointments by email
        cursor = db.appointments.find({"customer_email": email}).sort("date", 1)
        
        print("\n📋 Appointments found:")
        count = 0
        async for apt in cursor:
            count += 1
            print(f"  - Date: {apt.get('date')} | Time: {apt.get('time')} | Status: {apt.get('status')} | ID: {apt.get('_id')}")
            
        if count == 0:
            print("  No appointments found by email.")
            
            # Try by phone if email fails
            phone = "4434027219" 
            print(f"\n🔍 Searching by phone (fuzzy): {phone}")
            cursor = db.appointments.find({"phone": {"$regex": phone}})
            async for apt in cursor:
                print(f"  - Date: {apt.get('date')} | Time: {apt.get('time')} | Status: {apt.get('status')} | Phone: {apt.get('phone')}")

        print("\n✅ Inspection complete")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(inspect())
