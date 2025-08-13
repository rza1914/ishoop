from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.services.user_service import UserService
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    return current_user

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(User).offset(skip).limit(limit).all()
    return users
