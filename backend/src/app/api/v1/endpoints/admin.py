from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.models import User, Product, Order, Discount
from app.core.security import get_current_admin

router = APIRouter()

@router.get('/stats')
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    today = datetime.utcnow().date()
    
    total_users = db.query(User).count()
    total_products = db.query(Product).count()
    today_orders = db.query(Order).filter(
        func.date(Order.created_at) == today
    ).count()
    
    today_sales = db.query(func.sum(Order.total_amount)).filter(
        func.date(Order.created_at) == today
    ).scalar() or 0
    
    return {
        'total_users': total_users,
        'total_products': total_products,
        'today_orders': today_orders,
        'today_sales': today_sales
    }

@router.get('/sales-chart')
async def get_sales_chart_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    # داده‌های فروش برای 7 روز گذشته
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    sales_data = db.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total_amount).label('total')
    ).filter(
        Order.created_at >= start_date,
        Order.created_at <= end_date
    ).group_by(func.date(Order.created_at)).all()
    
    labels = []
    values = []
    
    # پر کردن داده‌های برای همه روزها (حتی روزهایی بدون فروش)
    for i in range(7):
        date = (start_date + timedelta(days=i)).date()
        labels.append(date.strftime('%Y-%m-%d'))
        
        # پیدا کردن فروش برای این روز
        day_sales = next((item.total for item in sales_data if item.date == date), 0)
        values.append(day_sales)
    
    return {
        'labels': labels,
        'values': values
    }

@router.get('/users')
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return db.query(User).offset(skip).limit(limit).all()

@router.get('/orders')
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return db.query(Order).offset(skip).limit(limit).all()

@router.get('/products')
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return db.query(Product).offset(skip).limit(limit).all()

@router.get('/discounts')
async def get_discounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    return db.query(Discount).offset(skip).limit(limit).all()
