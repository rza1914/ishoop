from fastapi import FastAPI, HTTPException, status, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sqlite3
import hashlib
import json
import random
import string
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="iShop API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = "ishop.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # برای دسترسی آسان به ستون‌ها
    return conn

def init_db():
    print("🗄️ راه‌اندازی دیتابیس...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image_url TEXT,
            category_id INTEGER,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL NOT NULL,
            status TEXT DEFAULT 'در حال پردازش',
            tracking_code TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Order items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Reviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Blog posts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            excerpt TEXT,
            content TEXT NOT NULL,
            image_url TEXT,
            is_published BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if data exists
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count == 0:
        print("📊 ایجاد داده‌های نمونه...")
        
        # Create admin user
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (email, name, password_hash, is_admin) VALUES (?, ?, ?, ?)",
            ("admin@ishop.com", "مدیر سیستم", admin_hash, 1)
        )
        
        # Create sample categories
        categories = [
            ("موبایل و تبلت", "گوشی‌های هوشمند و تبلت‌ها"),
            ("کامپیوتر", "لپ‌تاپ و کامپیوتر رومیزی"),
            ("صوتی", "هدفون و اسپیکر"),
            ("پوشیدنی", "ساعت هوشمند و دستبند")
        ]
        cursor.executemany(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            categories
        )
        
        # Sample products
        products = [
            ("گوشی Samsung Galaxy S24", "گوشی هوشمند پیشرفته با دوربین فوق‌العاده", 18000000, "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400", 1),
            ("آیفون 15 پرو", "جدیدترین گوشی اپل با چیپ A17 Pro", 45000000, "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400", 1),
            ("لپتاپ Dell XPS", "لپتاپ قدرتمند برای کار و بازی", 35000000, "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400", 2),
            ("مک‌بوک ایر M2", "لپتاپ اپل با چیپ M2", 48000000, "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400", 2),
            ("هدفون Sony WH-1000XM5", "هدفون بی‌سیم با حذف نویز", 8500000, "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400", 3),
            ("ایرپادز پرو", "هدفون بی‌سیم اپل", 9500000, "https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?w=400", 3),
            ("ساعت Apple Watch Series 9", "ساعت هوشمند اپل", 15000000, "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400", 4),
            ("ساعت Samsung Galaxy Watch", "ساعت هوشمند سامسونگ", 8000000, "https://images.unsplash.com/photo-1579586337278-3f436f25d4d6?w=400", 4)
        ]
        cursor.executemany(
            "INSERT INTO products (name, description, price, image_url, category_id) VALUES (?, ?, ?, ?, ?)",
            products
        )
        
        # Sample reviews
        reviews = [
            (1, 1, 5, "محصول فوق‌العاده! کیفیت ساخت عالی."),
            (1, 2, 4, "گران ولی ارزشش رو داره."),
            (1, 3, 5, "بهترین لپتاپی که تا حالا استفاده کردم."),
            (1, 4, 4, "طراحی زیبا و کارایی بالا."),
            (1, 5, 5, "کیفیت صدا فوق‌العاده!"),
        ]
        cursor.executemany(
            "INSERT INTO reviews (user_id, product_id, rating, text) VALUES (?, ?, ?, ?)",
            reviews
        )
        
        # Sample blog posts
        blog_posts = [
            (
                "راهنمای خرید گوشی هوشمند 2024",
                "همه چیزی که برای خرید گوشی جدید باید بدانید",
                "<h2>عوامل مهم در خرید گوشی</h2><p>برای خرید گوشی هوشمند جدید باید به عوامل مختلفی توجه کنید...</p>",
                "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600"
            ),
            (
                "مقایسه لپتاپ‌های 2024",
                "بررسی بهترین لپتاپ‌های سال",
                "<h2>معیارهای انتخاب لپتاپ</h2><p>برای انتخاب لپتاپ مناسب باید نیازهای خود را بشناسید...</p>",
                "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600"
            ),
            (
                "آینده ساعت‌های هوشمند",
                "نگاهی به تکنولوژی‌های آینده",
                "<h2>تکنولوژی‌های نوظهور</h2><p>ساعت‌های هوشمند آینده قابلیت‌های شگفت‌انگیزی خواهند داشت...</p>",
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600"
            )
        ]
        cursor.executemany(
            "INSERT INTO blog_posts (title, excerpt, content, image_url) VALUES (?, ?, ?, ?)",
            blog_posts
        )
        
        print("✅ داده‌های نمونه ایجاد شد")
    
    conn.commit()
    conn.close()
    print("✅ دیتابیس آماده است")

# Models
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class OrderCreate(BaseModel):
    total: float
    items: List[dict]

class ReviewCreate(BaseModel):
    product_id: int
    rating: int
    text: Optional[str] = None

# Helper functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_tracking_code() -> str:
    return "ISH" + ''.join(random.choices(string.digits, k=8))

def authenticate_user(token: str = None):
    # ساده‌ترین authentication برای تست
    if not token or not token.startswith("token-"):
        return None
    
    try:
        user_id = int(token.replace("token-", ""))
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "is_admin": bool(user["is_admin"])
            }
    except:
        pass
    return None

# Routes
@app.get("/")
async def root():
    return {"message": "🛍️ iShop API با SQLite Database آماده است!"}

@app.post("/api/v1/auth/login")
async def login(username: str = Form(), password: str = Form()):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ایمیل یا رمز عبور اشتباه است"
        )
    
    return {
        "access_token": f"token-{user['id']}",
        "token_type": "bearer"
    }

@app.post("/api/v1/auth/register")
async def register(user_data: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # بررسی وجود کاربر
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="این ایمیل قبلاً ثبت شده است")
    
    # ایجاد کاربر جدید
    password_hash = hash_password(user_data.password)
    cursor.execute(
        "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
        (user_data.email, user_data.name, password_hash)
    )
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "access_token": f"token-{user_id}",
        "token_type": "bearer"
    }

@app.get("/api/v1/users/me")
async def get_current_user():
    # برای سادگی، کاربر ادمین رو برمی‌گردونیم
    return {
        "id": 1,
        "email": "admin@ishop.com",
        "name": "مدیر سیستم",
        "is_admin": True
    }

@app.get("/api/v1/categories")
async def get_categories():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    conn.close()
    
    return [dict(cat) for cat in categories]

@app.get("/api/v1/products")
async def get_products(category_id: Optional[int] = None, search: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.is_active = 1
    """
    params = []
    
    if category_id:
        query += " AND p.category_id = ?"
        params.append(category_id)
    
    if search:
        query += " AND (p.name LIKE ? OR p.description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    query += " ORDER BY p.created_at DESC"
    
    cursor.execute(query, params)
    products = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "description": p["description"],
            "price": p["price"],
            "imageUrl": p["image_url"],
            "category": p["category_name"] or "بدون دسته",
            "created_at": p["created_at"]
        }
        for p in products
    ]

@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get product
    cursor.execute("""
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        WHERE p.id = ?
    """, (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        raise HTTPException(status_code=404, detail="محصول یافت نشد")
    
    # Get reviews
    cursor.execute("""
        SELECT r.*, u.name as author_name 
        FROM reviews r 
        JOIN users u ON r.user_id = u.id 
        WHERE r.product_id = ? 
        ORDER BY r.created_at DESC
    """, (product_id,))
    reviews = cursor.fetchall()
    
    conn.close()
    
    return {
        "id": product["id"],
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "imageUrl": product["image_url"],
        "category": product["category_name"] or "بدون دسته",
        "reviews": [
            {
                "id": r["id"],
                "author": r["author_name"],
                "rating": r["rating"],
                "text": r["text"],
                "created_at": r["created_at"]
            }
            for r in reviews
        ]
    }

@app.get("/api/v1/orders")
async def get_orders():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT o.*, u.name as customer_name,
               GROUP_CONCAT(p.name, ', ') as product_names
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN products p ON oi.product_id = p.id
        GROUP BY o.id
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": o["id"],
            "customer_name": o["customer_name"],
            "total": o["total"],
            "status": o["status"],
            "tracking_code": o["tracking_code"],
            "date": o["created_at"],
            "items": [{"product_name": name} for name in (o["product_names"] or "").split(", ") if name]
        }
        for o in orders
    ]

@app.post("/api/v1/orders")
async def create_order(order_data: OrderCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    tracking_code = generate_tracking_code()
    
    # Create order
    cursor.execute(
        "INSERT INTO orders (user_id, total, tracking_code) VALUES (?, ?, ?)",
        (1, order_data.total, tracking_code)  # user_id = 1 برای تست
    )
    order_id = cursor.lastrowid
    
    # Create order items
    for item in order_data.items:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, item["product_id"], item["quantity"], item.get("price", 0))
        )
    
    conn.commit()
    conn.close()
    
    return {
        "id": order_id,
        "tracking_code": tracking_code,
        "status": "در حال پردازش",
        "message": "سفارش با موفقیت ثبت شد"
    }

@app.post("/api/v1/reviews")
async def create_review(review_data: ReviewCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO reviews (user_id, product_id, rating, text) VALUES (?, ?, ?, ?)",
        (1, review_data.product_id, review_data.rating, review_data.text)  # user_id = 1 برای تست
    )
    review_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": review_id,
        "message": "نظر شما با موفقیت ثبت شد"
    }

@app.get("/api/v1/blog")
async def get_blog_posts():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM blog_posts WHERE is_published = 1 ORDER BY created_at DESC"
    )
    posts = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": p["id"],
            "title": p["title"],
            "excerpt": p["excerpt"],
            "content": p["content"],
            "imageUrl": p["image_url"],
            "date": p["created_at"]
        }
        for p in posts
    ]

@app.get("/api/v1/blog/{post_id}")
async def get_blog_post(post_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM blog_posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()
    conn.close()
    
    if not post:
        raise HTTPException(status_code=404, detail="مطلب یافت نشد")
    
    return {
        "id": post["id"],
        "title": post["title"],
        "excerpt": post["excerpt"],
        "content": post["content"],
        "imageUrl": post["image_url"],
        "date": post["created_at"]
    }

@app.get("/api/v1/users")
async def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, email, name, is_admin, created_at FROM users")
    users = cursor.fetchall()
    conn.close()
    
    return [dict(user) for user in users]

# Initialize database on startup
init_db()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting iShop API with SQLite Database...")
    print("🌐 API: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    print("👤 Admin: admin@ishop.com / admin123")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)