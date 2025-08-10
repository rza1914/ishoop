# app/api/v1/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.api.dependencies import get_current_user
from datetime import datetime

router = APIRouter()

# Sample orders storage
SAMPLE_ORDERS = []

@router.post("/")
async def create_order(
    order_data: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new order"""
    try:
        new_order = {
            "id": len(SAMPLE_ORDERS) + 1,
            "user_id": current_user["id"],
            "order_number": f"ORD-{len(SAMPLE_ORDERS) + 1:06d}",
            "items": order_data.get("items", []),
            "total_amount": order_data.get("total_amount", 0),
            "shipping_address": order_data.get("shipping_address", {}),
            "payment_method": order_data.get("payment_method", "card"),
            "status": "pending",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        SAMPLE_ORDERS.append(new_order)
        return new_order
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_user_orders(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's orders"""
    try:
        user_orders = [order for order in SAMPLE_ORDERS if order["user_id"] == current_user["id"]]
        return user_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# app/api/v1/reviews.py - Reviews Router
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.api.dependencies import get_current_user
from datetime import datetime

reviews_router = APIRouter()

# Sample reviews storage
SAMPLE_REVIEWS = []

@reviews_router.post("/")
async def create_review(
    review_data: dict,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new product review"""
    try:
        new_review = {
            "id": len(SAMPLE_REVIEWS) + 1,
            "user_id": current_user["id"],
            "user": {
                "id": current_user["id"],
                "full_name": current_user["full_name"]
            },
            "product_id": review_data.get("product_id"),
            "rating": review_data.get("rating", 5),
            "comment": review_data.get("comment", ""),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        SAMPLE_REVIEWS.append(new_review)
        return new_review
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@reviews_router.get("/")
async def get_reviews(
    product_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Get reviews for a product"""
    try:
        if product_id:
            product_reviews = [review for review in SAMPLE_REVIEWS if review["product_id"] == product_id]
            return product_reviews
        return SAMPLE_REVIEWS
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))