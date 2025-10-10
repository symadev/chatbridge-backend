from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    def connect_db(cls):
        """establish the MongoDB connection """
        mongodb_url = os.getenv("MONGODB_URL")
        cls.client = AsyncIOMotorClient(mongodb_url)
        print(" Connected to MongoDB!")
    
    @classmethod
    def close_db(cls):
        """MongoDB connection close করো"""
        if cls.client:
            cls.client.close()
            print(" MongoDB connection closed")
    
    @classmethod
    def get_database(cls):
        """Database instance return করো"""
        return cls.client.ChatBridge  # Database name
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Specific collection return করো"""
        db = cls.get_database()
        return db[collection_name]

# Shortcut functions
def get_users_collection():
    return MongoDB.get_collection("users")

def get_messages_collection():
    return MongoDB.get_collection("messages")