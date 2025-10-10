from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserLogin, UserResponse
from app.database.mongodb import get_users_collection
from app.utils.password import hash_password, verify_password
from app.utils.auth import create_access_token
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    """User registration"""
    users_collection = get_users_collection()
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and save user
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(user_data)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(result.inserted_id)})
    
    return {
        "message": "User created successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=dict)
async def login(user: UserLogin):
    """User login"""
    users_collection = get_users_collection()
    
    # Find user
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(db_user["_id"])})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user["username"]
    }