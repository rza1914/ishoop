from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
async def get_current_user_info(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information"""
    try:
        # Remove password hash from response
        user_info = {
            "id": current_user["id"],
            "email": current_user["email"],
            "full_name": current_user["full_name"],
            "is_active": current_user["is_active"],
            "created_at": current_user["created_at"]
        }
        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))