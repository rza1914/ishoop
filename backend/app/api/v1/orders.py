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