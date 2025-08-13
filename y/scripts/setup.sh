#!/bin/bash

echo "🚀 راه‌اندازی پروژه iShop..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker نصب نیست. لطفاً ابتدا Docker را نصب کنید."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose نصب نیست. لطفاً ابتدا Docker Compose را نصب کنید."
    exit 1
fi

echo "📦 ساخت و اجرای کانتینرها..."
docker-compose up --build -d

echo "⏳ انتظار برای آماده شدن دیتابیس..."
sleep 10

echo "🗄️ اجرای مایگریشن‌ها..."
docker-compose exec backend python -c "
from app.db.database import engine
from app.models import *
from app.models.user import User
from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.review import Review
from app.models.blog import BlogPost
from app.db.database import Base
Base.metadata.create_all(bind=engine)
print('✅ جداول دیتابیس ایجاد شد')
"

echo "🌱 ایجاد داده‌های اولیه..."
docker-compose exec backend python -c "
import random
import string
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

# Create admin user
admin = User(
    email='admin@ishop.com',
    name='مدیر سیستم',
    hashed_password=get_password_hash('admin123'),
    is_admin=True
)
db.add(admin)
db.commit()
print('✅ کاربر ادمین ایجاد شد (admin@ishop.com / admin123)')

db.close()
"

echo "✅ پروژه آماده است!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "🔑 اطلاعات ورود ادمین:"
echo "Email: admin@ishop.com"
echo "Password: admin123"
