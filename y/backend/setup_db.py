import os
import sys
from app.db.database import engine
from app.models.user import User
from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.blog import BlogPost
from app.db.database import Base, SessionLocal
from app.core.security import get_password_hash

def create_tables():
    print("📊 ایجاد جداول...")
    Base.metadata.create_all(bind=engine)
    print("✅ جداول ایجاد شد")

def create_admin_user():
    print("👤 ایجاد کاربر ادمین...")
    db = SessionLocal()
    
    # بررسی وجود ادمین
    existing_admin = db.query(User).filter(User.email == "admin@ishop.com").first()
    if existing_admin:
        print("ℹ️ کاربر ادمین از قبل موجود است")
        db.close()
        return
    
    # ایجاد ادمین جدید
    admin = User(
        email="admin@ishop.com",
        name="مدیر سیستم",
        hashed_password=get_password_hash("admin123"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print("✅ کاربر ادمین ایجاد شد:")
    print("   Email: admin@ishop.com")
    print("   Password: admin123")
    db.close()

def create_sample_data():
    print("🛍️ ایجاد داده‌های نمونه...")
    db = SessionLocal()
    
    # ایجاد دسته‌بندی نمونه
    if not db.query(Category).first():
        category = Category(
            name="الکترونیک",
            description="محصولات الکترونیکی"
        )
        db.add(category)
        db.commit()
        
        # ایجاد محصول نمونه
        product = Product(
            name="گوشی هوشمند",
            description="گوشی هوشمند با کیفیت بالا",
            price=15000000,
            image_url="https://via.placeholder.com/300x200?text=Phone",
            category_id=category.id
        )
        db.add(product)
        db.commit()
        print("✅ داده‌های نمونه ایجاد شد")
    
    db.close()

if __name__ == "__main__":
    print("🚀 راه‌اندازی iShop...")
    create_tables()
    create_admin_user()
    create_sample_data()
    print("🎉 راه‌اندازی کامل شد!")
    print("🌐 حالا سرور رو اجرا کن: python main.py")
