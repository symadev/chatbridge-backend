from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatMessage(BaseModel):
    """Chat message model"""
    user_id: str
    message: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatMessageInDB(ChatMessage):
    """ it will save to the Database """
    id: str = Field(alias="_id")
    
    class Config:
        populate_by_name = True

class ChatMessageResponse(BaseModel):
    """Response model"""
    id: str
    message: str
    response: str
    timestamp: datetime