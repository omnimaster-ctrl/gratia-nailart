"""
Shared database module for Gratia Nail Art.
Single MongoDB connection pool used by all backend modules.
Database name is determined by MONGO_DB_NAME environment variable.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'gratia_nailart_db')

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
