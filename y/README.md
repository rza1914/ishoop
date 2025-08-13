# 🛍️ iShop - فروشگاه آنلاین مدرن

فروشگاه آنلاین کامل با React مدرن و FastAPI

## ✨ ویژگی‌ها

### 🎨 فرانت‌اند مدرن
- ✅ React 18 با Hooks
- ✅ Tailwind CSS با Glassmorphism
- ✅ Framer Motion برای انیمیشن‌ها
- ✅ React Query برای مدیریت state
- ✅ طراحی responsive و موبایل‌فرندلی
- ✅ Dark/Light theme support
- ✅ PWA ready

### 🚀 بک‌اند قدرتمند
- ✅ FastAPI با Python 3.11
- ✅ PostgreSQL database
- ✅ Redis برای cache
- ✅ JWT Authentication
- ✅ SQLAlchemy ORM
- ✅ Automatic API documentation
- ✅ OAuth integration ready

### 🔐 امنیت
- ✅ JWT Token authentication
- ✅ Password hashing با bcrypt
- ✅ CORS configuration
- ✅ Input validation
- ✅ SQL injection protection

### 📱 قابلیت‌ها
- ✅ مدیریت محصولات
- ✅ سیستم سبد خرید
- ✅ پنل ادمین کامل
- ✅ سیستم نظردهی
- ✅ وبلاگ
- ✅ جستجو و فیلتر پیشرفته

## 🚀 راه‌اندازی سریع

### پیش‌نیازها
- Docker & Docker Compose
- Git

### نصب با Docker (توصیه شده)
```bash
# Clone the repository
git clone <repository-url>
cd ishop

# اجرای اسکریپت راه‌اندازی
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### نصب محیط توسعه
```bash
# اجرای محیط توسعه
chmod +x scripts/dev.sh
./scripts/dev.sh
```

## 🌐 دسترسی‌ها

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: PostgreSQL on port 5432

## 🔑 اطلاعات پیش‌فرض

### کاربر ادمین
- **Email**: admin@ishop.com
- **Password**: admin123

## 📁 ساختار پروژه

```
ishop/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── db/             # Database connection
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── main.py
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API services
│   │   └── styles/         # CSS styles
│   └── package.json
├── database/               # Database migrations
├── scripts/                # Setup scripts
├── docs/                   # Documentation
└── docker-compose.yml      # Docker configuration
```

## 🛠️ توسعه

### Backend Commands
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Commands
```bash
cd frontend
npm install
npm start
```

### Database Migration
```bash
# ایجاد migration جدید
alembic revision --autogenerate -m "migration message"

# اجرای migration
alembic upgrade head
```

## 📚 API Documentation

API documentation در آدرس http://localhost:8000/docs در دسترس است.

### مهم‌ترین Endpoints:
- `POST /api/v1/auth/login` - ورود کاربر
- `POST /api/v1/auth/register` - ثبت‌نام کاربر
- `GET /api/v1/products` - لیست محصولات
- `POST /api/v1/orders` - ثبت سفارش
- `GET /api/v1/users/me` - اطلاعات کاربر

## 🧪 تست

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📦 Production Deployment

### با Docker
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment
1. Set environment variables
2. Build frontend: `npm run build`
3. Run backend: `uvicorn main:app --host 0.0.0.0 --port 8000`

## 🤝 مشارکت

1. Fork کنید
2. Branch جدید بسازید
3. تغییرات را commit کنید
4. Push کنید
5. Pull Request ایجاد کنید

## 📄 License

MIT License

## 📞 پشتیبانی

برای سوالات و پشتیبانی:
- ایمیل: support@ishop.com
- تلگرام: @ishop_support

---

**ساخته شده با ❤️ برای کسب‌وکارهای ایرانی**
