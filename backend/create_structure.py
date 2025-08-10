#!/usr/bin/env python3
import os
from pathlib import Path

# ساختار دایرکتوری‌ها
directories = [
    'app',
    'static/css',
    'static/js',
    'static/img',
    'templates',
    'tests'
]

# فایل‌ها با محتوای اولیه
files = {
    'app/__init__.py': '''# این فایل به پایتون می‌گوید که این پوشه یک پکیج است
''',

    'app/main.py': '''from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from pathlib import Path

app = FastAPI(debug=True)  # فعال کردن حالت دیباگ

# مسیر پروژه
BASE_DIR = Path(__file__).resolve().parent.parent

# استاتیک‌ها و تمپلیت‌ها
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# مسیر اصلی
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        return templates.TemplateResponse("home.html", {"request": request})
    except Exception as e:
        print(f"Error rendering template: {e}")
        return HTMLResponse(content=f"<h1>Error: {str(e)}</h1>", status_code=500)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
''',

    'app/database.py': '''import sqlite3
from contextlib import contextmanager

DATABASE_URL = "ishoop.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            is_admin BOOLEAN DEFAULT 0
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            category TEXT
        )
        """)
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
''',

    'app/auth.py': '''from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import random

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def generate_otp():
    return str(random.randint(100000, 999999))
''',

    'app/crud.py': '''from .database import get_db
from .models import Product, User, Order
from typing import List, Optional

def get_products(db, skip: int = 0, limit: int = 100):
    return db.execute("SELECT * FROM products LIMIT ? OFFSET ?", (limit, skip)).fetchall()

def get_product(db, product_id: int):
    return db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()

def create_product(db, product: Product):
    db.execute(
        "INSERT INTO products (name, price, stock, category) VALUES (?, ?, ?, ?)",
        (product.name, product.price, product.stock, product.category)
    )
    db.commit()

def get_user_by_phone(db, phone: str):
    return db.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()

def create_user(db, phone: str, is_admin: bool = False):
    db.execute(
        "INSERT INTO users (phone, is_admin) VALUES (?, ?)",
        (phone, is_admin)
    )
    db.commit()
''',

    'app/models.py': '''from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    phone: str

class UserCreate(UserBase):
    is_admin: bool = False

class User(UserBase):
    id: int
    is_admin: bool
    
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    total: float

class OrderCreate(OrderBase):
    products: List[int]

class Order(OrderBase):
    id: int
    status: str
    
    class Config:
        orm_mode = True
''',

    'static/css/style.css': '''/* استایل‌های سفارشی */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* استایل‌های شیشه‌ای */
.glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
''',

    'static/js/ishoop.js': '''class IShoop {
    constructor() {
        this.apiBase = "/api";
        this.token = localStorage.getItem("token") || "";
        this.cart = JSON.parse(localStorage.getItem("cart")) || [];
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
        }
        return data;
    }

    // محصولات
    async getProducts() {
        const response = await fetch(`${this.apiBase}/products`);
        return response.json();
    }

    async getProduct(id) {
        const response = await fetch(`${this.apiBase}/products/${id}`);
        return response.json();
    }

    // سبد خرید
    addToCart(productId) {
        if (!this.cart.includes(productId)) {
            this.cart.push(productId);
            localStorage.setItem("cart", JSON.stringify(this.cart));
            this.updateCartUI();
        }
    }

    removeFromCart(productId) {
        this.cart = this.cart.filter(id => id !== productId);
        localStorage.setItem("cart", JSON.stringify(this.cart));
        this.updateCartUI();
    }

    updateCartUI() {
        document.getElementById("cart-count").textContent = this.cart.length;
    }

    // UI
    init() {
        this.updateCartUI();
    }
}

// مقداردهی اولیه
document.addEventListener("DOMContentLoaded", () => {
    window.ishoop = new IShoop();
    window.ishoop.init();
});
''',

    'static/js/admin.js': '''// اسکریپت‌های پنل مدیریت
document.addEventListener("DOMContentLoaded", () => {
    // مدیریت تب‌ها
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");
    
    tabButtons.forEach(button => {
        button.addEventListener("click", () => {
            const tabId = button.getAttribute("data-tab");
            
            // غیرفعال کردن همه تب‌ها
            tabButtons.forEach(btn => btn.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));
            
            // فعال کردن تب انتخاب شده
            button.classList.add("active");
            document.getElementById(`tab-${tabId}`).classList.add("active");
            
            // بارگذاری محتوای تب
            loadTabContent(tabId);
        });
    });
    
    // بارگذاری محتوای تب‌ها
    async function loadTabContent(tabId) {
        const contentDiv = document.getElementById(`tab-${tabId}`);
        contentDiv.innerHTML = "<p>در حال بارگذاری...</p>";
        
        try {
            const response = await fetch(`/api/admin/${tabId}`);
            const data = await response.json();
            renderTabContent(tabId, data);
        } catch (error) {
            contentDiv.innerHTML = "<p>خطا در بارگذاری داده‌ها</p>";
        }
    }
    
    function renderTabContent(tabId, data) {
        const contentDiv = document.getElementById(`tab-${tabId}`);
        // منطق رندر محتوا بر اساس تب
        // ...
    }
});
''',

    'templates/base.html': '''<!DOCTYPE html>
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
    <header class="glass p-4 mb-6">
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
</html>
''',

    'templates/home.html': '''{% extends "base.html" %}

{% block title %}iShoop - فروشگاه آنلاین{% endblock %}

{% block content %}
<div class="glass rounded-xl p-6 mb-8">
    <h1 class="text-3xl font-bold text-indigo-800 mb-4">به iShoop خوش آمدید!</h1>
    <p class="text-lg text-indigo-700">بهترین محصولات با بهترین قیمت‌ها</p>
</div>

<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="glass rounded-xl p-6">
        <h2 class="text-xl font-bold text-indigo-800 mb-2">محصولات جدید</h2>
        <p class="text-indigo-700">جدیدترین محصولات را بررسی کنید</p>
        <a href="/products" class="mt-4 inline-block bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">مشاهده محصولات</a>
    </div>
    
    <div class="glass rounded-xl p-6">
        <h2 class="text-xl font-bold text-indigo-800 mb-2">تخفیف‌های ویژه</h2>
        <p class="text-indigo-700">تخفیف‌های باورنکردنی را از دست ندهید</p>
        <a href="/products?discount=true" class="mt-4 inline-block bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">تخفیف‌ها</a>
    </div>
    
    <div class="glass rounded-xl p-6">
        <h2 class="text-xl font-bold text-indigo-800 mb-2">درباره ما</h2>
        <p class="text-indigo-700">با iShoop بیشتر آشنا شوید</p>
        <a href="/about" class="mt-4 inline-block bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">بیشتر بدانید</a>
    </div>
</div>
{% endblock %}
''',

    'static/img/favicon.ico': '''# این یک فایل باینری است
# شما می‌توانید یک فایل favicon واقعی جایگزین آن کنید
# یا از یک سرویس آنلاین برای ایجاد favicon استفاده کنید
''',

    'requirements.txt': '''fastapi>=0.104.0
uvicorn>=0.24.0
jinja2>=3.1.2
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.5
pydantic>=2.7.0
pydantic-settings>=2.0.0
''',

    # بقیه فایل‌ها مانند قبل ...
}

# ایجاد دایرکتوری‌ها
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# ایجاد فایل‌ها با محتوای اولیه
for file_path, content in files.items():
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("✅ ساختار پروژه iShoop با موفقیت ایجاد شد!")
print("\nبرای شروع:")
print("1. دیتابیس را مقداردهی اولیه کنید: python app/database.py")
print("2. وابستگی‌ها را نصب کنید: pip install -r requirements.txt --upgrade")
print("3. سرور را اجرا کنید: python -m uvicorn app.main:app --reload")
print("   یا: python app/main.py")
print("4. در مرورگر به آدرس http://localhost:8000 بروید")