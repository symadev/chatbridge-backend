from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    """for the login"""
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    """save it the database"""
    id: str = Field(alias="_id")
    username: str
    email: str
    hashed_password: str
    created_at: datetime
    
    class Config:
        populate_by_name = True

class UserResponse(BaseModel):
    """what it send as a response"""
    id: str
    username: str
    email: str