from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.product import Product, ProductCreate
from app.crud.product import product_crud
from app.api.dependencies import get_current_user

router = APIRouter()

# Sample products data for initial testing
SAMPLE_PRODUCTS = [
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
    },
    {
        "id": 6,
        "name": "ساعت هوشمند Apple Watch",
        "description": "ساعت هوشمند با امکانات سلامتی پیشرفته",
        "price": 15000000,
        "category": "پوشیدنی",
        "stock_quantity": 12,
        "image_url": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400"
    }
]

@router.get("/", response_model=List[dict])
async def get_products(db: Session = Depends(get_db)):
    """Get all products"""
    try:
        # For now, return sample data
        # Later you can implement: return product_crud.get_products(db)
        return SAMPLE_PRODUCTS
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    try:
        # Find product in sample data
        product = next((p for p in SAMPLE_PRODUCTS if p["id"] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=dict)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new product (requires authentication)"""
    try:
        # For now, just return the created product with a new ID
        new_product = {
            "id": len(SAMPLE_PRODUCTS) + 1,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "stock_quantity": product.stock_quantity,
            "image_url": product.image_url
        }
        SAMPLE_PRODUCTS.append(new_product)
        return new_product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))