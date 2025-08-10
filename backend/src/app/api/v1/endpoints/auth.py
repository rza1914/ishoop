from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.session import get_db
from app.schemas.user import UserCreate, User, Token
from app.core.security import create_access_token, verify_password, get_password_hash
from typing import Dict

router = APIRouter()

# Sample users database (in real app, this would be in database)
SAMPLE_USERS = []

@router.post("/register", response_model=Dict[str, str])
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = next((u for u in SAMPLE_USERS if u["email"] == user.email), None)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )
        
        # Create new user
        new_user = {
            "id": len(SAMPLE_USERS) + 1,
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": get_password_hash(user.password),
            "is_active": True,
            "created_at": datetime.now()
        }
        
        SAMPLE_USERS.append(new_user)
        
        return {"message": "User registered successfully", "email": user.email}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return access token"""
    try:
        # Find user by email (username in form_data is actually email)
        user = next((u for u in SAMPLE_USERS if u["email"] == form_data.username), None)
        
        if not user or not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))