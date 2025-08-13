#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows Fix Script برای iShop
این اسکریپت مشکلات ویندوز رو حل می‌کنه
"""

import os
import sys
from pathlib import Path

def fix_config_file():
    """اصلاح فایل config برای Pydantic v2"""
    config_content = """from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "iShop"
    
    # Database - SQLite برای Windows
    DATABASE_URL: str = "sqlite:///./ishop.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-please-make-it-very-long-and-random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis (Optional for Windows)
    REDIS_URL: Optional[str] = None
    
    # Email (Optional)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
"""
    
    config_path = Path("backend/app/core/config.py")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    print("✅ فایل config اصلاح شد")

def fix_requirements():
    """اصلاح requirements.txt برای Windows"""
    requirements_content = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
bcrypt==4.1.2
python-decouple==3.8
aiofiles==23.2.1
httpx==0.25.2
pydantic-settings==2.0.3
email-validator==2.1.0
"""
    
    req_path = Path("backend/requirements.txt")
    with open(req_path, 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    print("✅ فایل requirements اصلاح شد")

def fix_database_file():
    """اصلاح فایل database برای SQLite"""
    database_content = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLite برای ویندوز
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}  # فقط برای SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
    
    db_path = Path("backend/app/db/database.py")
    with open(db_path, 'w', encoding='utf-8') as f:
        f.write(database_content)
    print("✅ فایل database اصلاح شد")

def create_simple_startup_script():
    """ایجاد اسکریپت ساده راه‌اندازی"""
    startup_content = """import os
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
"""
    
    startup_path = Path("backend/setup_db.py")
    with open(startup_path, 'w', encoding='utf-8') as f:
        f.write(startup_content)
    print("✅ اسکریپت راه‌اندازی ایجاد شد")

def create_frontend_config():
    """ایجاد کانفیگ فرانت برای ویندوز"""
    env_content = """REACT_APP_API_URL=http://localhost:8000
GENERATE_SOURCEMAP=false
BROWSER=none
"""
    
    frontend_env = Path("frontend/.env")
    with open(frontend_env, 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ کانفیگ فرانت ایجاد شد")

def run_fixes():
    """اجرای تمام اصلاحات"""
    print("🔧 شروع اصلاح مشکلات ویندوز...")
    
    # بررسی مسیر
    if not Path("backend").exists():
        print("❌ پوشه backend یافت نشد. مطمئن شوید در پوشه پروژه هستید.")
        return False
    
    try:
        fix_config_file()
        fix_requirements()
        fix_database_file()
        create_simple_startup_script()
        create_frontend_config()
        
        print("\n🎉 تمام مشکلات برطرف شد!")
        print("\n📋 مراحل بعدی:")
        print("1. cd backend")
        print("2. pip install -r requirements.txt")
        print("3. python setup_db.py")
        print("4. python main.py")
        print("\n🆕 تب جدید PowerShell باز کن:")
        print("1. cd frontend")
        print("2. npm install")
        print("3. npm start")
        print("\n🌐 سایت: http://localhost:3000")
        print("🔗 API: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

if __name__ == "__main__":
    run_fixes()