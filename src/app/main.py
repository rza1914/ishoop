from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="iShop API",
    description="API for iShop e-commerce platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# In-memory storage (for simplicity)
products_db = [
    {
        "id": 1,
        "name": "آیفون 15 پرو مکس",
        "description": "جدیدترین مدل آیفون اپل با کیفیت بی‌نظیر",
        "price": 45000000,
        "category": "موبایل",
        "stock_quantity": 10,
        "image_url": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400"
    },
    {
        "id": 2,
        "name": "سامسونگ Galaxy S24",
        "description": "گوشی هوشمند سامسونگ با قابلیت‌های پیشرفته",
        "price": 35000000,
        "category": "موبایل",
        "stock_quantity": 15,
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"
    },
    {
        "id": 3,
        "name": "لپ‌تاپ MacBook Pro",
        "description": "لپ‌تاپ قدرتمند اپل برای کار حرفه‌ای",
        "price": 75000000,
        "category": "لپ‌تاپ",
        "stock_quantity": 5,
        "image_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400"
    },
    {
        "id": 4,
        "name": "هدفون Sony WH-1000XM5",
        "description": "هدفون بی‌سیم با کیفیت صدای عالی",
        "price": 8500000,
        "category": "صوتی",
        "stock_quantity": 20,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
    },
    {
        "id": 5,
        "name": "تبلت iPad Air",
        "description": "تبلت قدرتمند اپل برای کار و سرگرمی",
        "price": 25000000,
        "category": "تبلت",
        "stock_quantity": 8,
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400"
    }
]

users_db = []
orders_db = []
reviews_db = []

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to iShop API!", "status": "running", "version": "1.0.0"}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "products_count": len(products_db)}

# ===== PRODUCTS ENDPOINTS =====

@app.get("/api/v1/products/")
async def get_products():
    """Get all products"""
    return products_db

@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: int):
    """Get product by ID"""
    for product in products_db:
        if product["id"] == product_id:
            return product
    return {"detail": "Product not found"}

# ===== AUTH ENDPOINTS =====

@app.post("/api/v1/auth/register")
async def register(user_data: dict):
    """Register a new user"""
    email = user_data.get("email")
    password = user_data.get("password")
    full_name = user_data.get("full_name")
    
    if not email or not password or not full_name:
        return {"detail": "Missing required fields"}
    
    # Check if user exists
    for user in users_db:
        if user["email"] == email:
            return {"detail": "User already exists"}
    
    # Create new user
    new_user = {
        "id": len(users_db) + 1,
        "email": email,
        "full_name": full_name,
        "password": password,  # In real app, hash this!
        "is_active": True
    }
    
    users_db.append(new_user)
    return {"message": "User registered successfully", "email": email}

@app.post("/api/v1/auth/login")
async def login(credentials: dict):
    """Login user"""
    username = credentials.get("username") or credentials.get("email")
    password = credentials.get("password")
    
    if not username or not password:
        return {"detail": "Missing username or password"}
    
    # Find user
    for user in users_db:
        if user["email"] == username and user["password"] == password:
            return {
                "access_token": f"token_{user['id']}",
                "token_type": "bearer"
            }
    
    return {"detail": "Invalid credentials"}

# ===== USER ENDPOINTS =====

@app.get("/api/v1/users/me")
async def get_current_user():
    """Get current user info (simplified)"""
    if users_db:
        user = users_db[-1]  # Return last registered user for demo
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "is_active": user["is_active"]
        }
    return {"detail": "No user found"}

# ===== REVIEWS ENDPOINTS =====

@app.post("/api/v1/reviews/")
async def create_review(review_data: dict):
    """Create product review"""
    product_id = review_data.get("product_id")
    rating = review_data.get("rating", 5)
    comment = review_data.get("comment", "")
    
    if not product_id:
        return {"detail": "Product ID required"}
    
    new_review = {
        "id": len(reviews_db) + 1,
        "product_id": product_id,
        "rating": rating,
        "comment": comment,
        "user": {"id": 1, "full_name": "کاربر تست"},
        "created_at": "2024-01-01T00:00:00"
    }
    
    reviews_db.append(new_review)
    return new_review

@app.get("/api/v1/reviews/")
async def get_reviews(product_id: int = None):
    """Get reviews"""
    if product_id:
        result = []
        for review in reviews_db:
            if review["product_id"] == product_id:
                result.append(review)
        return result
    return reviews_db

# ===== ORDERS ENDPOINTS =====

@app.post("/api/v1/orders/")
async def create_order(order_data: dict):
    """Create new order"""
    items = order_data.get("items", [])
    total_amount = order_data.get("total_amount", 0)
    shipping_address = order_data.get("shipping_address", {})
    
    new_order = {
        "id": len(orders_db) + 1,
        "order_number": f"ORD-{len(orders_db) + 1:06d}",
        "items": items,
        "total_amount": total_amount,
        "shipping_address": shipping_address,
        "status": "pending",
        "created_at": "2024-01-01T00:00:00"
    }
    
    orders_db.append(new_order)
    return new_order

@app.get("/api/v1/orders/")
async def get_orders():
    """Get all orders"""
    return orders_db

# Debug endpoint to see all data
@app.get("/debug")
async def debug_data():
    """Debug endpoint to see all stored data"""
    return {
        "products": len(products_db),
        "users": len(users_db),
        "orders": len(orders_db),
        "reviews": len(reviews_db),
        "sample_product": products_db[0] if products_db else None
    }
    # ======= ADMIN ENDPOINTS =======
# این کدها رو به انتهای main.py اضافه کنید

from datetime import datetime

# Admin authentication middleware (ساده)
def get_current_admin_user(token: str = None):
    """ساده‌ترین حالت چک admin - فقط برای demo"""
    # در production باید role-based authentication باشد
    if not token or not token.startswith("token_"):
        return None
    return {"id": 1, "email": "admin@ishop.com", "role": "admin"}

# ===== ADMIN DASHBOARD ENDPOINTS =====

@app.get("/admin")
async def admin_dashboard():
    """صفحه اصلی Admin Panel"""
    return {
        "message": "Welcome to iShop Admin Panel",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/api/v1/admin/stats")
async def admin_stats():
    """آمار کلی برای Dashboard"""
    return {
        "total_products": len(products_db),
        "total_users": len(users_db),
        "total_orders": len(orders_db),
        "total_reviews": len(reviews_db),
        "revenue": sum([order.get("total_amount", 0) for order in orders_db]),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/v1/admin/dashboard")
async def admin_dashboard_data():
    """داده‌های کامل Dashboard"""
    recent_orders = orders_db[-5:] if len(orders_db) >= 5 else orders_db
    recent_users = users_db[-5:] if len(users_db) >= 5 else users_db
    
    return {
        "stats": {
            "products": len(products_db),
            "users": len(users_db),
            "orders": len(orders_db),
            "reviews": len(reviews_db)
        },
        "recent_orders": recent_orders,
        "recent_users": [{"id": u["id"], "email": u["email"], "full_name": u["full_name"]} for u in recent_users],
        "charts": {
            "orders_by_month": [{"month": "Jan", "count": 5}, {"month": "Feb", "count": 8}],
            "revenue_by_month": [{"month": "Jan", "revenue": 1000000}, {"month": "Feb", "revenue": 1500000}]
        }
    }

@app.get("/api/v1/admin/reports")
async def admin_reports():
    """گزارشات مختلف"""
    return {
        "sales_report": {
            "total_sales": len(orders_db),
            "total_revenue": sum([order.get("total_amount", 0) for order in orders_db]),
            "avg_order_value": sum([order.get("total_amount", 0) for order in orders_db]) / len(orders_db) if orders_db else 0
        },
        "product_report": {
            "total_products": len(products_db),
            "categories": list(set([p.get("category") for p in products_db if p.get("category")])),
            "low_stock": [p for p in products_db if p.get("stock_quantity", 0) < 10]
        },
        "user_report": {
            "total_users": len(users_db),
            "active_users": len([u for u in users_db if u.get("is_active", True)]),
            "new_users_today": 0  # simplified
        }
    }

# ===== ADMIN PRODUCT MANAGEMENT =====

@app.post("/api/v1/admin/products")
async def admin_create_product(product_data: dict):
    """ایجاد محصول جدید توسط Admin"""
    new_product = {
        "id": len(products_db) + 1,
        "name": product_data.get("name"),
        "description": product_data.get("description"),
        "price": product_data.get("price"),
        "category": product_data.get("category"),
        "stock_quantity": product_data.get("stock_quantity", 0),
        "image_url": product_data.get("image_url"),
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    products_db.append(new_product)
    return new_product

@app.get("/api/v1/admin/products")
async def admin_get_products():
    """دریافت تمام محصولات برای Admin"""
    # Add admin-only fields
    admin_products = []
    for product in products_db:
        admin_product = product.copy()
        admin_product.update({
            "sales_count": 0,  # simplified
            "revenue": 0,      # simplified
            "status": "active"
        })
        admin_products.append(admin_product)
    
    return {
        "products": admin_products,
        "total": len(admin_products),
        "categories": list(set([p.get("category") for p in products_db if p.get("category")]))
    }

@app.get("/api/v1/admin/products/{product_id}")
async def admin_get_product(product_id: int):
    """جزئیات محصول برای Admin"""
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        return {"detail": "Product not found"}
    
    # Add admin-specific data
    admin_product = product.copy()
    admin_product.update({
        "views": 0,
        "sales_count": 0,
        "revenue": 0,
        "reviews_count": len([r for r in reviews_db if r.get("product_id") == product_id]),
        "avg_rating": 4.5  # simplified
    })
    
    return admin_product

@app.put("/api/v1/admin/products/{product_id}")
async def admin_update_product(product_id: int, product_data: dict):
    """ویرایش محصول توسط Admin"""
    for i, product in enumerate(products_db):
        if product["id"] == product_id:
            products_db[i].update({
                "name": product_data.get("name", product["name"]),
                "description": product_data.get("description", product["description"]),
                "price": product_data.get("price", product["price"]),
                "category": product_data.get("category", product["category"]),
                "stock_quantity": product_data.get("stock_quantity", product["stock_quantity"]),
                "image_url": product_data.get("image_url", product["image_url"]),
                "updated_at": datetime.now().isoformat()
            })
            return products_db[i]
    
    return {"detail": "Product not found"}

@app.delete("/api/v1/admin/products/{product_id}")
async def admin_delete_product(product_id: int):
    """حذف محصول توسط Admin"""
    global products_db
    products_db = [p for p in products_db if p["id"] != product_id]
    return {"message": "Product deleted successfully"}

@app.patch("/api/v1/admin/products/{product_id}/inventory")
async def admin_update_inventory(product_id: int, inventory_data: dict):
    """به‌روزرسانی موجودی"""
    for product in products_db:
        if product["id"] == product_id:
            product["stock_quantity"] = inventory_data.get("stock_quantity", product["stock_quantity"])
            product["updated_at"] = datetime.now().isoformat()
            return {"message": "Inventory updated", "new_stock": product["stock_quantity"]}
    
    return {"detail": "Product not found"}

# ===== ADMIN USER MANAGEMENT =====

@app.get("/api/v1/admin/users")
async def admin_get_users(search: str = None):
    """دریافت تمام کاربران"""
    filtered_users = users_db
    
    if search:
        filtered_users = [u for u in users_db 
                         if search.lower() in u.get("email", "").lower() or 
                            search.lower() in u.get("full_name", "").lower()]
    
    # Remove sensitive data
    safe_users = []
    for user in filtered_users:
        safe_user = {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "is_active": user.get("is_active", True),
            "created_at": datetime.now().isoformat(),  # simplified
            "last_login": datetime.now().isoformat(),  # simplified
            "orders_count": len([o for o in orders_db if o.get("user_id") == user["id"]])
        }
        safe_users.append(safe_user)
    
    return {
        "users": safe_users,
        "total": len(safe_users),
        "active": len([u for u in safe_users if u.get("is_active", True)])
    }

@app.get("/api/v1/admin/users/stats")
async def admin_user_stats():
    """آمار کاربران"""
    return {
        "total_users": len(users_db),
        "active_users": len([u for u in users_db if u.get("is_active", True)]),
        "new_users_this_month": len(users_db),  # simplified
        "users_with_orders": len(set([o.get("user_id") for o in orders_db if o.get("user_id")])),
        "top_customers": [
            {"user_id": 1, "orders": 5, "revenue": 1000000},
            {"user_id": 2, "orders": 3, "revenue": 750000}
        ]
    }

@app.get("/api/v1/admin/roles")
async def admin_get_roles():
    """دریافت نقش‌های کاربران"""
    return {
        "roles": [
            {"id": 1, "name": "admin", "description": "Administrator"},
            {"id": 2, "name": "user", "description": "Regular User"},
            {"id": 3, "name": "moderator", "description": "Content Moderator"}
        ]
    }

# ===== ADMIN ORDER MANAGEMENT =====

@app.get("/api/v1/admin/orders")
async def admin_get_orders(status: str = None):
    """دریافت تمام سفارشات"""
    filtered_orders = orders_db
    
    if status:
        filtered_orders = [o for o in orders_db if o.get("status") == status]
    
    # Add admin-specific data
    admin_orders = []
    for order in filtered_orders:
        admin_order = order.copy()
        admin_order.update({
            "customer_name": "مشتری تست",  # simplified
            "customer_email": "customer@test.com",  # simplified
            "payment_status": "paid",
            "shipping_status": "pending"
        })
        admin_orders.append(admin_order)
    
    return {
        "orders": admin_orders,
        "total": len(admin_orders),
        "statuses": ["pending", "processing", "shipped", "delivered", "cancelled"]
    }

@app.get("/api/v1/admin/orders/stats")
async def admin_order_stats():
    """آمار سفارشات"""
    return {
        "total_orders": len(orders_db),
        "pending_orders": len([o for o in orders_db if o.get("status") == "pending"]),
        "completed_orders": len([o for o in orders_db if o.get("status") == "completed"]),
        "total_revenue": sum([o.get("total_amount", 0) for o in orders_db]),
        "avg_order_value": sum([o.get("total_amount", 0) for o in orders_db]) / len(orders_db) if orders_db else 0,
        "orders_today": 0,  # simplified
        "revenue_today": 0   # simplified
    }

@app.get("/api/v1/admin/sales/report")
async def admin_sales_report():
    """گزارش فروش"""
    return {
        "summary": {
            "total_sales": len(orders_db),
            "total_revenue": sum([o.get("total_amount", 0) for o in orders_db]),
            "avg_order_value": sum([o.get("total_amount", 0) for o in orders_db]) / len(orders_db) if orders_db else 0
        },
        "by_month": [
            {"month": "2024-01", "sales": 10, "revenue": 5000000},
            {"month": "2024-02", "sales": 15, "revenue": 7500000}
        ],
        "by_category": [
            {"category": "موبایل", "sales": 8, "revenue": 3000000},
            {"category": "لپ‌تاپ", "sales": 5, "revenue": 4000000}
        ],
        "top_products": [
            {"product_id": 1, "name": "آیفون 15 پرو مکس", "sales": 5, "revenue": 2250000},
            {"product_id": 2, "name": "سامسونگ Galaxy S24", "sales": 3, "revenue": 1050000}
        ]
    }

# ===== ADMIN ANALYTICS =====

@app.get("/api/v1/admin/analytics/overview")
async def admin_analytics_overview():
    """بررسی کلی Analytics"""
    return {
        "period": "last_30_days",
        "metrics": {
            "page_views": 15420,
            "unique_visitors": 3241,
            "conversion_rate": 2.3,
            "bounce_rate": 45.2,
            "avg_session_duration": "00:03:24"
        },
        "trends": {
            "visitors_change": "+12.5%",
            "orders_change": "+8.3%",
            "revenue_change": "+15.7%"
        }
    }

@app.get("/api/v1/admin/analytics/sales-monthly")
async def admin_monthly_sales():
    """گزارش فروش ماهانه"""
    return {
        "chart_data": [
            {"month": "Jan 2024", "sales": 120, "revenue": 60000000},
            {"month": "Feb 2024", "sales": 150, "revenue": 75000000},
            {"month": "Mar 2024", "sales": 180, "revenue": 90000000}
        ],
        "growth": "+25%",
        "best_month": "Mar 2024"
    }

@app.get("/api/v1/admin/analytics/popular-products")
async def admin_popular_products():
    """محبوب‌ترین محصولات"""
    return {
        "products": [
            {"id": 1, "name": "آیفون 15 پرو مکس", "views": 1250, "sales": 45, "revenue": 2025000},
            {"id": 2, "name": "سامسونگ Galaxy S24", "views": 980, "sales": 32, "revenue": 1120000}
        ]
    }

@app.get("/api/v1/admin/analytics/active-users")
async def admin_active_users():
    """آمار کاربران فعال"""
    return {
        "daily_active": 234,
        "weekly_active": 1420,
        "monthly_active": 4567,
        "returning_users": "68%",
        "new_users": "32%"
    }

# ===== ADMIN SETTINGS =====

# Simple settings storage
admin_settings = {
    "site_name": "iShop",
    "maintenance_mode": False,
    "allow_registration": True,
    "admin_email": "admin@ishop.com"
}

@app.get("/api/v1/admin/settings")
async def admin_get_settings():
    """دریافت تنظیمات سایت"""
    return admin_settings

@app.put("/api/v1/admin/settings")
async def admin_update_settings(settings_data: dict):
    """به‌روزرسانی تنظیمات"""
    admin_settings.update(settings_data)
    return {"message": "Settings updated successfully", "settings": admin_settings}

@app.post("/api/v1/admin/backup")
async def admin_create_backup():
    """ایجاد نسخه پشتیبان"""
    backup_data = {
        "products": len(products_db),
        "users": len(users_db),
        "orders": len(orders_db),
        "reviews": len(reviews_db),
        "created_at": datetime.now().isoformat(),
        "size": "2.3 MB"
    }
    return {"message": "Backup created successfully", "backup": backup_data}

# ===== ADMIN CONTENT MANAGEMENT =====

# Simple categories storage
categories_db = [
    {"id": 1, "name": "موبایل", "description": "گوشی‌های هوشمند"},
    {"id": 2, "name": "لپ‌تاپ", "description": "کامپیوترهای قابل حمل"}
]

@app.post("/api/v1/admin/categories")
async def admin_create_category(category_data: dict):
    """ایجاد دسته‌بندی جدید"""
    new_category = {
        "id": len(categories_db) + 1,
        "name": category_data.get("name"),
        "description": category_data.get("description"),
        "created_at": datetime.now().isoformat()
    }
    categories_db.append(new_category)
    return new_category

@app.get("/api/v1/admin/categories")
async def admin_get_categories():
    """دریافت تمام دسته‌بندی‌ها"""
    return {"categories": categories_db, "total": len(categories_db)}

@app.get("/api/v1/admin/brands")
async def admin_get_brands():
    """دریافت برندها"""
    return {
        "brands": [
            {"id": 1, "name": "Apple", "products_count": 3},
            {"id": 2, "name": "Samsung", "products_count": 2},
            {"id": 3, "name": "Sony", "products_count": 1}
        ]
    }

# ===== ADMIN SECURITY =====

# Simple activity log
activity_logs = []

@app.get("/api/v1/admin/activity-logs")
async def admin_activity_logs():
    """لاگ فعالیت‌های Admin"""
    sample_logs = [
        {"id": 1, "user": "admin@ishop.com", "action": "Created Product", "timestamp": datetime.now().isoformat()},
        {"id": 2, "user": "admin@ishop.com", "action": "Updated Settings", "timestamp": datetime.now().isoformat()}
    ]
    return {"logs": sample_logs, "total": len(sample_logs)}

@app.get("/api/v1/admin/failed-logins")
async def admin_failed_logins():
    """تلاش‌های ورود ناموفق"""
    return {
        "failed_attempts": [
            {"ip": "192.168.1.100", "email": "hacker@test.com", "timestamp": datetime.now().isoformat()},
            {"ip": "10.0.0.50", "email": "test@test.com", "timestamp": datetime.now().isoformat()}
        ],
        "total": 2,
        "blocked_ips": ["192.168.1.100"]
    }

@app.get("/api/v1/admin/security/stats")
async def admin_security_stats():
    """آمار امنیتی"""
    return {
        "total_logins": 45,
        "failed_logins": 3,
        "blocked_ips": 1,
        "suspicious_activity": 0,
        "last_admin_login": datetime.now().isoformat(),
        "security_score": 85
    }