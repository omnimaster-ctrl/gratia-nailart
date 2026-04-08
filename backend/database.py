"""
Shared database module.
Single MongoDB connection pool used by all backend modules.
Database name is determined by MONGO_DB_NAME environment variable
to support multi-tenant deployments.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'lapopnails_db')

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
