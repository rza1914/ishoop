from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.db.session import get_db
from app.models.models import Product, Order, OrderItem, Review

def get_popular_products(db: Session, limit: int = 10) -> List[Product]:
    # محصولات پرفروش بر اساس تعداد فروش
    popular_products = db.query(
        Product.id,
        Product.name,
        Product.price,
        func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).join(Order).group_by(Product.id).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(limit).all()
    
    return [db.query(Product).filter(Product.id == p.id).first() for p in popular_products]

def get_similar_products(db: Session, product_id: int, limit: int = 5) -> List[Product]:
    # محصولات مشابه بر اساس دسته‌بندی
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return []
    
    similar_products = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product_id
    ).limit(limit).all()
    
    return similar_products

def get_user_recommendations(db: Session, user_id: int, limit: int = 10) -> List[Product]:
    # پیشنهاد محصولات بر اساس سابقه خرید کاربر
    user_orders = db.query(Order).filter(Order.user_id == user_id).all()
    
    if not user_orders:
        return get_popular_products(db, limit)
    
    # پیدا کردن دسته‌بندی‌های محصولات خریداری شده
    categories = set()
    for order in user_orders:
        for item in order.items:
            if item.product.category:
                categories.add(item.product.category)
    
    # پیشنهاد محصولات از همان دسته‌بندی‌ها
    recommended_products = db.query(Product).filter(
        Product.category.in_(categories)
    ).limit(limit).all()
    
    return recommended_products
