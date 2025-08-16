from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    products = relationship("Product", back_populates="category")
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Category name must be at least 2 characters")
        return name.strip()

class Product(Base):
    __tablename__ = "products"
    
    __table_args__ = (
        CheckConstraint('price > 0', name='positive_price'),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(500))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    is_active = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    sku = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Product name must be at least 2 characters")
        return name.strip()
    
    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be positive")
        return price
    
    @hybrid_property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    @hybrid_property
    def review_count(self):
        return len(self.reviews)
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0
