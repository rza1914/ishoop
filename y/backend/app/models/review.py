from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from app.db.database import Base

class Review(Base):
    __tablename__ = "reviews"
    
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating'),
        UniqueConstraint('user_id', 'product_id', name='unique_user_product_review')
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    title = Column(String(200))
    text = Column(Text)
    is_verified_purchase = Column(Integer, default=0)  # Boolean as int for SQLite
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        return rating
    
    @validates('text')
    def validate_text(self, key, text):
        if text and len(text.strip()) < 5:
            raise ValueError("Review text must be at least 5 characters")
        return text.strip() if text else text
