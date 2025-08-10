from .database import get_db
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
