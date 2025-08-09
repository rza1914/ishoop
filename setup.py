#!/usr/bin/env python3
import os
import subprocess
import sys

def run_command(command):
    """اجرای دستورات ترمینال"""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return result

def create_file(path, content):
    """ایجاد فایل با محتوای مشخص"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

# 1. ایجاد ساختار پروژه
print("=== ایجاد ساختار پروژه ===")
directories = [
    'app/api/endpoints',
    'app/core',
    'app/db',
    'app/models',
    'app/schemas',
    'app/services',
    'static/css',
    'static/js',
    'static/img',
    'templates',
    'tests',
    'migrations'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

# 2. ایجاد فایل‌های اصلی
print("\n=== ایجاد فایل‌های اصلی ===")

# فایل requirements.txt
create_file('requirements.txt', '''fastapi>=0.104.0
uvicorn>=0.24.0
jinja2>=3.1.2
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.5
pydantic>=2.7.0
pydantic-settings>=2.0.0
redis>=4.5.0
fastapi-cache2>=0.2.0
fastapi-limiter>=0.1.5
websockets>=11.0.0
sqlalchemy>=2.0.0
alembic>=1.12.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
''')

# فایل .env
create_file('.env', '''# تنظیمات پایگاه داده
DATABASE_URL=sqlite:///./ishoop.db

# تنظیمات احراز هویت
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# تنظیمات Redis
REDIS_URL=redis://localhost:6379

# تنظیمات OTP
OTP_EXPIRE_MINUTES=5

# تنظیمات پرداخت
PAYMENT_GATEWAY=zarinpal
MERCHANT_ID=your-merchant-id

# تنظیمات ایمیل
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
''')

# فایل Dockerfile
create_file('Dockerfile', '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# فایل docker-compose.yml
create_file('docker-compose.yml', '''version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379
    volumes:
      - .:/app

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  db:
    image: sqlite:latest
    volumes:
      - ./data:/data
''')

# 3. ایجاد ماژول‌های بک‌اند
print("\n=== ایجاد ماژول‌های بک‌اند ===")

# فایل app/main.py
create_file('app/main.py', '''from fastapi import FastAPI, Request, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from pathlib import Path

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

app = FastAPI(
    title="iShoop API",
    description="API for iShoop e-commerce platform",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# استاتیک‌ها و تمپلیت‌ها
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# ایجاد جداول پایگاه داده
Base.metadata.create_all(bind=engine)

# اتصال به Redis
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# مسیر اصلی
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# WebSocket برای اعلان‌ها
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

# شامل روت‌های API
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
''')

# فایل app/core/config.py
create_file('app/core/config.py', '''from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./ishoop.db"
    SECRET_KEY: str = "your-super-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: str = "redis://localhost:6379"
    OTP_EXPIRE_MINUTES: int = 5
    PAYMENT_GATEWAY: str = "zarinpal"
    MERCHANT_ID: str = "your-merchant-id"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
''')

# فایل app/db/session.py
create_file('app/db/session.py', '''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

# فایل app/models/models.py
create_file('app/models/models.py', '''from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base

class UserRole(enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, index=True)
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    order_items = relationship("OrderItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # روابط
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
    # روابط
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_id = Column(String, unique=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    order = relationship("Order", back_populates="payment")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # روابط
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

class Discount(Base):
    __tablename__ = "discounts"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    percentage = Column(Float, nullable=False)
    max_uses = Column(Integer, default=1)
    used_count = Column(Integer, default=0)
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
''')

# 4. ایجاد فایل‌های فرانت‌اند
print("\n=== ایجاد فایل‌های فرانت‌اند ===")

# فایل templates/base.html
create_file('templates/base.html', '''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}iShoop{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.ico">
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
    <header class="glass p-4 mb-6 sticky top-0 z-50">
        <div class="container mx-auto flex justify-between items-center">
            <div class="text-2xl font-bold text-indigo-800">iShoop</div>
            <nav>
                <ul class="flex space-x-reverse space-x-4">
                    <li><a href="/" class="text-indigo-700 hover:text-indigo-900">خانه</a></li>
                    <li><a href="/products" class="text-indigo-700 hover:text-indigo-900">محصولات</a></li>
                    <li><a href="/cart" class="text-indigo-700 hover:text-indigo-900">سبد خرید (<span id="cart-count">0</span>)</a></li>
                    <li><a href="/auth" class="text-indigo-700 hover:text-indigo-900">ورود</a></li>
                    <li><a href="/admin" class="text-indigo-700 hover:text-indigo-900">مدیریت</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container mx-auto px-4">
        {% block content %}{% endblock %}
    </main>

    <footer class="glass mt-12 p-4">
        <div class="container mx-auto text-center text-indigo-700">
            © 2023 iShoop - تمامی حقوق محفوظ است
        </div>
    </footer>

    <script src="/static/js/ishoop.js"></script>
</body>
</html>''')

# فایل static/css/style.css
create_file('static/css/style.css', '''/* استایل‌های سفارشی */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* استایل‌های شیشه‌ای */
.glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* استایل‌های لود تنقل تصاویر */
.lazyload {
    opacity: 0;
    transition: opacity 0.3s;
}

.lazyloaded {
    opacity: 1;
}

/* استایل‌های انیمیشن */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* استایل‌های ویجت‌ها */
.widget {
    @apply glass rounded-xl p-6 mb-6 transition-all duration-300 hover:shadow-lg;
}

/* استایل‌های دکمه‌ها */
.btn {
    @apply px-4 py-2 rounded-lg transition-colors duration-300;
}

.btn-primary {
    @apply bg-indigo-600 text-white hover:bg-indigo-700;
}

.btn-secondary {
    @apply bg-gray-200 text-gray-800 hover:bg-gray-300;
}

.btn-danger {
    @apply bg-red-600 text-white hover:bg-red-700;
}

/* استایل‌های فرم‌ها */
.form-group {
    @apply mb-4;
}

.form-label {
    @apply block text-indigo-700 mb-2;
}

.form-input {
    @apply w-full p-3 rounded-lg border border-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-500;
}

/* استایل‌های کارت‌ها */
.card {
    @apply glass rounded-xl p-4 transition-all duration-300 hover:shadow-lg;
}

/* استایل‌های تب‌ها */
.tab-btn {
    @apply px-4 py-2 rounded-lg transition-colors duration-300;
}

.tab-btn.active {
    @apply bg-indigo-600 text-white;
}

.tab-content {
    @apply hidden;
}

.tab-content.active {
    @apply block;
}

/* استایل‌های اعلان‌ها */
.notification {
    @apply fixed bottom-4 right-4 glass rounded-xl p-4 max-w-md shadow-lg z-50;
}

.notification.success {
    @apply border-green-500;
}

.notification.error {
    @apply border-red-500;
}

.notification.info {
    @apply border-blue-500;
}
''')

# فایل static/js/ishoop.js
create_file('static/js/ishoop.js', '''class IShoop {
    constructor() {
        this.apiBase = "/api/v1";
        this.token = localStorage.getItem("token") || "";
        this.cart = JSON.parse(localStorage.getItem("cart")) || [];
        this.user = JSON.parse(localStorage.getItem("user")) || null;
        this.notifications = [];
        this.websocket = null;
    }

    // احراز هویت
    async sendOTP(phone) {
        const response = await fetch(`${this.apiBase}/auth/send-otp`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({phone})
        });
        return response.json();
    }

    async verifyOTP(phone, otp) {
        const response = await fetch(`${this.apiBase}/auth/verify-otp`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({phone, otp})
        });
        const data = await response.json();
        if (data.access_token) {
            this.token = data.access_token;
            localStorage.setItem("token", this.token);
            await this.getCurrentUser();
        }
        return data;
    }

    async getCurrentUser() {
        if (!this.token) return null;
        
        const response = await fetch(`${this.apiBase}/users/me`, {
            headers: {"Authorization": `Bearer ${this.token}`}
        });
        
        if (response.ok) {
            this.user = await response.json();
            localStorage.setItem("user", JSON.stringify(this.user));
            return this.user;
        } else {
            this.logout();
            return null;
        }
    }

    logout() {
        this.token = "";
        this.user = null;
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/";
    }

    // محصولات
    async getProducts(filters = {}) {
        const params = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key] !== undefined && filters[key] !== null) {
                params.append(key, filters[key]);
            }
        });
        
        const response = await fetch(`${this.apiBase}/products?${params}`);
        return response.json();
    }

    async getProduct(id) {
        const response = await fetch(`${this.apiBase}/products/${id}`);
        return response.json();
    }

    async getPopularProducts() {
        const response = await fetch(`${this.apiBase}/products/popular`);
        return response.json();
    }

    async getRecommendedProducts() {
        if (!this.user) return [];
        
        const response = await fetch(`${this.apiBase}/products/recommended`, {
            headers: {"Authorization": `Bearer ${this.token}`}
        });
        return response.json();
    }

    // سبد خرید
    addToCart(productId) {
        if (!this.cart.includes(productId)) {
            this.cart.push(productId);
            localStorage.setItem("cart", JSON.stringify(this.cart));
            this.updateCartUI();
            this.showNotification("محصول به سبد خرید اضافه شد", "success");
        }
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(id => id !== productId);
        localStorage.setItem("cart", JSON.stringify(this.cart));
        this.updateCartUI();
        this.showNotification("محصول از سبد خرید حذف شد", "info");
    }

    async getCartItems() {
        const items = [];
        for (const productId of this.cart) {
            const product = await this.getProduct(productId);
            items.push(product);
        }
        return items;
    }

    updateCartUI() {
        const cartCount = document.getElementById("cart-count");
        if (cartCount) {
            cartCount.textContent = this.cart.length;
        }
    }

    // سفارشات
    async createOrder(items) {
        const response = await fetch(`${this.apiBase}/orders`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${this.token}`
            },
            body: JSON.stringify({items})
        });
        return response.json();
    }

    async getOrders() {
        const response = await fetch(`${this.apiBase}/orders`, {
            headers: {"Authorization": `Bearer ${this.token}`}
        });
        return response.json();
    }

    // پرداخت
    async createPayment(orderId) {
        const response = await fetch(`${this.apiBase}/payments`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${this.token}`
            },
            body: JSON.stringify({order_id: orderId})
        });
        return response.json();
    }

    // نظرات
    async addReview(productId, rating, comment) {
        const response = await fetch(`${this.apiBase}/reviews`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${this.token}`
            },
            body: JSON.stringify({product_id: productId, rating, comment})
        });
        return response.json();
    }

    async getProductReviews(productId) {
        const response = await fetch(`${this.apiBase}/reviews?product_id=${productId}`);
        return response.json();
    }

    // تخفیف‌ها
    async validateDiscount(code) {
        const response = await fetch(`${this.apiBase}/discounts/validate`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({code})
        });
        return response.json();
    }

    // WebSocket برای اعلان‌ها
    connectWebSocket() {
        if (this.user && !this.websocket) {
            this.websocket = new WebSocket(`ws://localhost:8000/ws/${this.user.id}`);
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.showNotification(data.message, data.type || "info");
            };
            
            this.websocket.onclose = () => {
                this.websocket = null;
                setTimeout(() => this.connectWebSocket(), 5000);
            };
        }
    }

    // اعلان‌ها
    showNotification(message, type = "info") {
        const notification = document.createElement("div");
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // UI
    init() {
        this.updateCartUI();
        this.getCurrentUser();
        this.connectWebSocket();
        
        // لود تنقل تصاویر
        if ("IntersectionObserver" in window) {
            const lazyImages = document.querySelectorAll("img.lazyload");
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.add("lazyloaded");
                        observer.unobserve(img);
                    }
                });
            });
            
            lazyImages.forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
}

// مقداردهی اولیه
document.addEventListener("DOMContentLoaded", () => {
    window.ishoop = new IShoop();
    window.ishoop.init();
});
''')

# 5. ایجاد فایل‌های باقی‌مانده
print("\n=== ایجاد فایل‌های باقی‌مانده ===")

# فایل app/crud/__init__.py
create_file('app/crud/__init__.py', '')

# فایل app/api/api_v1/__init__.py
create_file('app/api/api_v1/__init__.py', '')

# فایل app/api/api_v1/endpoints/__init__.py
create_file('app/api/api_v1/endpoints/__init__.py', '')

# فایل static/img/favicon.ico
create_file('static/img/favicon.ico', '')

# فایل tests/__init__.py
create_file('tests/__init__.py', '')

# فایل alembic.ini
create_file('alembic.ini', '''[alembic]
script_location = migrations

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
''')

# فایل .gitignore
create_file('.gitignore', '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# Database files
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore
''')

# 6. ایجاد اسکریپت اجرایی
print("\n=== ایجاد اسکریپت اجرایی ===")

# فایل setup.py
create_file('setup.py', '''#!/usr/bin/env python3
import os
import sys
import subprocess

def run_command(command):
    """اجرای دستورات ترمینال"""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return result

def main():
    print("=== راه‌اندازی کامل iShoop ===")
    
    # 1. نصب وابستگی‌ها
    print("\\n1. نصب وابستگی‌ها...")
    run_command("pip install -r requirements.txt")
    
    # 2. ایجاد دیتابیس
    print("\\n2. ایجاد دیتابیس...")
    run_command("python -c 'from app.db.session import engine; from app.models.models import Base; Base.metadata.create_all(bind=engine)'")
    
    # 3. اجرای مهاجرت‌ها
    print("\\n3. اجرای مهاجرت‌ها...")
    run_command("alembic upgrade head")
    
    # 4. اجرای تست‌ها
    print("\\n4. اجرای تست‌ها...")
    run_command("pytest tests/ -v")
    
    # 5. اجرای سرور
    print("\\n5. اجرای سرور...")
    print("سرور در حال اجرا است... http://localhost:8000")
    run_command("uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")

if __name__ == "__main__":
    main()
''')
