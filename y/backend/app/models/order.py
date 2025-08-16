from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, CheckConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
import random
import string
from enum import Enum
from app.db.database import Base

def generate_tracking_code():
    """Generate unique tracking code"""
    return 'ISH' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Order(Base):
    __tablename__ = "orders"
    
    __table_args__ = (
        CheckConstraint('total >= 0', name='non_negative_total'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(String(20), default=OrderStatus.PENDING)
    tracking_code = Column(String(20), unique=True, index=True, default=generate_tracking_code)
    shipping_address = Column(Text)
    phone_number = Column(String(15))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    shipped_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    @validates('total')
    def validate_total(self, key, total):
        if total < 0:
            raise ValueError("Order total cannot be negative")
        return total
    
    @validates('status')
    def validate_status(self, key, status):
        if status not in [s.value for s in OrderStatus]:
            raise ValueError(f"Invalid order status: {status}")
        return status
    
    @hybrid_property
    def item_count(self):
        return sum(item.quantity for item in self.items)
    
    @property
    def can_be_cancelled(self):
        return self.status in [OrderStatus.PENDING, OrderStatus.PROCESSING]

class OrderItem(Base):
    __tablename__ = "order_items"
    
    __table_args__ = (
        CheckConstraint('quantity > 0', name='positive_quantity'),
        CheckConstraint('price >= 0', name='non_negative_price'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at time of order
    product_name = Column(String(200))  # Store name in case product is deleted
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
    
    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return quantity
    
    @validates('price')
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price
    
    @hybrid_property
    def subtotal(self):
        return self.quantity * self.price
