from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.review import Review
from app.schemas.review import Review as ReviewSchema, ReviewCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ReviewSchema)
def create_review(
    *,
    db: Session = Depends(get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    review_data = review_in.dict()
    review_data["user_id"] = current_user.id
    review = Review(**review_data)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
