from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.order import Order
from app.schemas.order import Order as OrderSchema, OrderCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[OrderSchema])
def read_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    if current_user.is_admin:
        orders = db.query(Order).all()
    else:
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.post("/", response_model=OrderSchema)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    order_data = order_in.dict()
    order_data["user_id"] = current_user.id
    order = Order(**order_data)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
