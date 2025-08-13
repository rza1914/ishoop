#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iShop Project Generator
ساخت کامل پروژه فروشگاه آنلاین با فرانت مدرن و بک‌اند FastAPI
"""

import os
import sys
import subprocess
from pathlib import Path

class iShopGenerator:
    def __init__(self, project_name="ishop"):
        self.project_name = project_name
        self.base_path = Path(project_name)
        
    def create_directory_structure(self):
        """ساخت ساختار فولدرها"""
        directories = [
            # Backend
            "backend",
            "backend/app",
            "backend/app/api",
            "backend/app/api/v1",
            "backend/app/api/v1/endpoints",
            "backend/app/core",
            "backend/app/db",
            "backend/app/models",
            "backend/app/schemas",
            "backend/app/services",
            "backend/app/utils",
            "backend/app/static",
            "backend/app/static/uploads",
            "backend/tests",
            
            # Frontend
            "frontend",
            "frontend/src",
            "frontend/src/components",
            "frontend/src/components/ui",
            "frontend/src/components/layout",
            "frontend/src/components/pages",
            "frontend/src/components/admin",
            "frontend/src/hooks",
            "frontend/src/services",
            "frontend/src/utils",
            "frontend/src/styles",
            "frontend/src/assets",
            "frontend/public",
            
            # Database
            "database",
            "database/migrations",
            
            # Docs
            "docs",
            
            # Scripts
            "scripts",
        ]
        
        for directory in directories:
            (self.base_path / directory).mkdir(parents=True, exist_ok=True)
        
        print("✅ ساختار فولدرها ایجاد شد")

    def create_backend_files(self):
        """ساخت فایل‌های بک‌اند"""
        
        # requirements.txt
        requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
bcrypt==4.1.2
python-decouple==3.8
redis==5.0.1
celery==5.3.4
pillow==10.1.0
aiofiles==23.2.1
httpx==0.25.2
pydantic-settings==2.0.3
"""
        self.write_file("backend/requirements.txt", requirements)
        
        # main.py
        main_py = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="iShop API",
    description="فروشگاه آنلاین iShop - API Documentation",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# API Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "iShop API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
"""
        self.write_file("backend/main.py", main_py)
        
        # Config
        config_py = """from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "iShop"
    
    # Database
    DATABASE_URL: str = "postgresql://ishop_user:ishop_pass@localhost/ishop_db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Email (for future use)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
"""
        self.write_file("backend/app/core/config.py", config_py)
        
        # Security
        security_py = """from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
"""
        self.write_file("backend/app/core/security.py", security_py)
        
        # Database
        database_py = """from sqlalchemy import create_engine
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
"""
        self.write_file("backend/app/db/database.py", database_py)
        
        # Models
        self.create_models()
        
        # Schemas
        self.create_schemas()
        
        # API Endpoints
        self.create_api_endpoints()
        
        print("✅ فایل‌های بک‌اند ایجاد شد")

    def create_models(self):
        """ساخت مدل‌های دیتابیس"""
        
        # User Model
        user_model = """from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
"""
        self.write_file("backend/app/models/user.py", user_model)
        
        # Product Model
        product_model = """from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
"""
        self.write_file("backend/app/models/product.py", product_model)
        
        # Order Model
        order_model = """from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid_property import hybrid_property
import random
import string
from app.db.database import Base

def generate_tracking_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Float, nullable=False)
    status = Column(String, default="در حال پردازش")
    tracking_code = Column(String, unique=True, index=True, default=generate_tracking_code)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at time of order
    
    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
"""
        self.write_file("backend/app/models/order.py", order_model)
        
        # Review Model
        review_model = """from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer, nullable=False)  # 1-5
    text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
"""
        self.write_file("backend/app/models/review.py", review_model)
        
        # Blog Model
        blog_model = """from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class BlogPost(Base):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    excerpt = Column(Text)
    content = Column(Text, nullable=False)
    image_url = Column(String)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
"""
        self.write_file("backend/app/models/blog.py", blog_model)
        
        # __init__.py for models
        models_init = """from .user import User
from .product import Product, Category
from .order import Order, OrderItem
from .review import Review
from .blog import BlogPost
"""
        self.write_file("backend/app/models/__init__.py", models_init)
        
        # Other necessary __init__.py files
        self.write_file("backend/app/__init__.py", "")
        self.write_file("backend/app/api/__init__.py", "")
        self.write_file("backend/app/api/v1/__init__.py", "")
        self.write_file("backend/app/api/v1/endpoints/__init__.py", "")
        self.write_file("backend/app/core/__init__.py", "")
        self.write_file("backend/app/db/__init__.py", "")
        self.write_file("backend/app/schemas/__init__.py", "")
        self.write_file("backend/app/services/__init__.py", "")
        self.write_file("backend/app/utils/__init__.py", "")

    def create_schemas(self):
        """ساخت Pydantic schemas"""
        
        # User Schemas
        user_schemas = """from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: Optional[int] = None
    is_active: bool = True
    is_admin: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
"""
        self.write_file("backend/app/schemas/user.py", user_schemas)
        
        # Product Schemas
        product_schemas = """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    is_active: bool = True
    created_at: datetime
    category: Optional[Category] = None

    class Config:
        from_attributes = True
"""
        self.write_file("backend/app/schemas/product.py", product_schemas)
        
        # Order Schemas
        order_schemas = """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    total: float
    status: str = "در حال پردازش"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    user_id: int
    tracking_code: Optional[str] = None
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True
"""
        self.write_file("backend/app/schemas/order.py", order_schemas)
        
        # Review Schemas
        review_schemas = """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    product_id: int
    rating: int
    text: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
"""
        self.write_file("backend/app/schemas/review.py", review_schemas)
        
        # Blog Schemas
        blog_schemas = """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogPostBase(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    is_published: bool = True

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
"""
        self.write_file("backend/app/schemas/blog.py", blog_schemas)
        
        # Token Schema
        token_schema = """from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
"""
        self.write_file("backend/app/schemas/token.py", token_schema)
        
        # Services
        user_service = """from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    @staticmethod
    def get(db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            name=obj_in.name,
            hashed_password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def update(
        db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def authenticate(db: Session, *, email: str, password: str) -> Optional[User]:
        user = UserService.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_admin(user: User) -> bool:
        return user.is_admin
"""
        self.write_file("backend/app/services/user_service.py", user_service)

    def create_api_endpoints(self):
        """ساخت API endpoints"""
        
        # Auth endpoints
        auth_endpoints = """from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import User as UserSchema, UserCreate
from app.services.user_service import UserService

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = UserService.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserSchema)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> Any:
    user = UserService.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = UserService.create(db, obj_in=user_in)
    return user
"""
        self.write_file("backend/app/api/v1/endpoints/auth.py", auth_endpoints)
        
        # Products endpoints
        products_endpoints = """from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.product import Product
from app.schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def read_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.post("/", response_model=ProductSchema)
def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: ProductCreate,
) -> Any:
    product = Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/{id}", response_model=ProductSchema)
def read_product(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{id}", response_model=ProductSchema)
def update_product(
    *,
    db: Session = Depends(get_db),
    id: int,
    product_in: ProductUpdate,
) -> Any:
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{id}")
def delete_product(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
"""
        self.write_file("backend/app/api/v1/endpoints/products.py", products_endpoints)
        
        # Users endpoints
        users_endpoints = """from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema
from app.services.user_service import UserService
from app.core.deps import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserSchema)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    return current_user

@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.query(User).offset(skip).limit(limit).all()
    return users
"""
        self.write_file("backend/app/api/v1/endpoints/users.py", users_endpoints)
        
        # Orders endpoints
        orders_endpoints = """from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.order import Order
from app.schemas.order import Order as OrderSchema, OrderCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[OrderSchema])
def read_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    if current_user.is_admin:
        orders = db.query(Order).all()
    else:
        orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.post("/", response_model=OrderSchema)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    order_data = order_in.dict()
    order_data["user_id"] = current_user.id
    order = Order(**order_data)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
"""
        self.write_file("backend/app/api/v1/endpoints/orders.py", orders_endpoints)
        
        # Reviews endpoints
        reviews_endpoints = """from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.review import Review
from app.schemas.review import Review as ReviewSchema, ReviewCreate
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ReviewSchema)
def create_review(
    *,
    db: Session = Depends(get_db),
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    review_data = review_in.dict()
    review_data["user_id"] = current_user.id
    review = Review(**review_data)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
"""
        self.write_file("backend/app/api/v1/endpoints/reviews.py", reviews_endpoints)
        
        # Blog endpoints
        blog_endpoints = """from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.blog import BlogPost
from app.schemas.blog import BlogPost as BlogPostSchema, BlogPostCreate, BlogPostUpdate

router = APIRouter()

@router.get("/", response_model=List[BlogPostSchema])
def read_blog_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    posts = db.query(BlogPost).filter(BlogPost.is_published == True).offset(skip).limit(limit).all()
    return posts

@router.get("/{id}", response_model=BlogPostSchema)
def read_blog_post(
    *,
    db: Session = Depends(get_db),
    id: int,
) -> Any:
    post = db.query(BlogPost).filter(BlogPost.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

@router.post("/", response_model=BlogPostSchema)
def create_blog_post(
    *,
    db: Session = Depends(get_db),
    post_in: BlogPostCreate,
) -> Any:
    post = BlogPost(**post_in.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
"""
        self.write_file("backend/app/api/v1/endpoints/blog.py", blog_endpoints)
        
        # Dependencies
        deps = """from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
"""
        self.write_file("backend/app/core/deps.py", deps)
        
        # Main API router
        api_router = """from fastapi import APIRouter
from app.api.v1.endpoints import auth, products, users, orders, reviews, blog

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(blog.router, prefix="/blog", tags=["blog"])
"""
        self.write_file("backend/app/api/v1/api.py", api_router)

    def create_frontend_files(self):
        """ساخت فایل‌های فرانت‌اند مدرن"""
        
        # package.json
        package_json = """{
  "name": "ishop-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "framer-motion": "^10.16.4",
    "react-query": "^3.39.3",
    "axios": "^1.6.0",
    "react-router-dom": "^6.8.0",
    "react-hook-form": "^7.47.0",
    "react-hot-toast": "^2.4.1",
    "lucide-react": "^0.292.0",
    "@headlessui/react": "^1.7.17",
    "tailwindcss": "^3.3.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "clsx": "^2.0.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}"""
        self.write_file("frontend/package.json", package_json)
        
        # Tailwind config
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'vazir': ['Vazirmatn', 'sans-serif'],
      },
      backdropBlur: {
        'xs': '2px',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'fade-in': 'fadeIn 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          'from': { boxShadow: '0 0 20px #667eea' },
          'to': { boxShadow: '0 0 30px #764ba2' },
        },
        slideUp: {
          'from': { transform: 'translateY(10px)', opacity: 0 },
          'to': { transform: 'translateY(0)', opacity: 1 },
        },
        slideDown: {
          'from': { transform: 'translateY(-10px)', opacity: 0 },
          'to': { transform: 'translateY(0)', opacity: 1 },
        },
        fadeIn: {
          'from': { opacity: 0 },
          'to': { opacity: 1 },
        },
        scaleIn: {
          'from': { transform: 'scale(0.9)', opacity: 0 },
          'to': { transform: 'scale(1)', opacity: 1 },
        },
      },
    },
  },
  plugins: [],
}"""
        self.write_file("frontend/tailwind.config.js", tailwind_config)
        
        # Modern App.js
        modern_app = """import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './hooks/useAuth';
import { CartProvider } from './hooks/useCart';
import Layout from './components/layout/Layout';
import HomePage from './components/pages/HomePage';
import ProductsPage from './components/pages/ProductsPage';
import ProductDetailPage from './components/pages/ProductDetailPage';
import AuthPage from './components/pages/AuthPage';
import DashboardPage from './components/pages/DashboardPage';
import AdminPage from './components/pages/AdminPage';
import BlogPage from './components/pages/BlogPage';
import './styles/globals.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <CartProvider>
          <Router>
            <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
              <Layout>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/products" element={<ProductsPage />} />
                  <Route path="/product/:id" element={<ProductDetailPage />} />
                  <Route path="/auth" element={<AuthPage />} />
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/admin" element={<AdminPage />} />
                  <Route path="/blog" element={<BlogPage />} />
                </Routes>
              </Layout>
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    background: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(20px)',
                    color: 'white',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                  },
                }}
              />
            </div>
          </Router>
        </CartProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;"""
        self.write_file("frontend/src/App.js", modern_app)
        
        # Global CSS
        global_css = """@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100;200;300;400;500;600;700;800;900&display=swap');
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  font-family: 'Vazirmatn', sans-serif;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Glass Effect Classes */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.glass-dark {
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.gradient-text {
  background: linear-gradient(135deg, #a2b2ee 0%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Hover Effects */
.hover-lift {
  transition: all 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.hover-glow:hover {
  box-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
}

/* Loading Animation */
.loading-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .glass {
    backdrop-filter: blur(15px);
  }
}"""
        self.write_file("frontend/src/styles/globals.css", global_css)
        
        print("✅ فایل‌های فرانت‌اند مدرن ایجاد شد")

    def create_docker_files(self):
        """ساخت فایل‌های Docker"""
        
        # Backend Dockerfile
        backend_dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]"""
        self.write_file("backend/Dockerfile", backend_dockerfile)
        
        # Frontend Dockerfile
        frontend_dockerfile = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]"""
        self.write_file("frontend/Dockerfile", frontend_dockerfile)
        
        # Docker Compose
        docker_compose = """version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ishop_db
      POSTGRES_USER: ishop_user
      POSTGRES_PASSWORD: ishop_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://ishop_user:ishop_pass@db/ishop_db
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:"""
        self.write_file("docker-compose.yml", docker_compose)
        
        print("✅ فایل‌های Docker ایجاد شد")

    def create_setup_scripts(self):
        """ساخت اسکریپت‌های راه‌اندازی"""
        
        # Setup script
        setup_script = r"""#!/bin/bash

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
"""
        self.write_file("scripts/setup.sh", setup_script)
        
        # Development script
        dev_script = r"""#!/bin/bash

echo "🔧 اجرای محیط توسعه..."

# Start services
docker-compose up -d db redis

echo "⏳ انتظار برای آماده شدن سرویس‌ها..."
sleep 5

# Start backend in development mode
echo "🚀 شروع Backend..."
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# Start frontend in development mode
echo "🎨 شروع Frontend..."
cd ../frontend
npm install
npm start &

echo "✅ محیط توسعه آماده است!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔗 Backend: http://localhost:8000"

wait"""
        self.write_file("scripts/dev.sh", dev_script)
        
        # Make scripts executable
        os.chmod(self.base_path / "scripts/setup.sh", 0o755)
        os.chmod(self.base_path / "scripts/dev.sh", 0o755)
        
        print("✅ اسکریپت‌های راه‌اندازی ایجاد شد")

    def create_readme(self):
        """ساخت فایل README"""
        
        readme = r"""# 🛍️ iShop - فروشگاه آنلاین مدرن

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
"""
        self.write_file("README.md", readme)
        print("✅ فایل README ایجاد شد")

    def create_env_files(self):
        """ساخت فایل‌های environment"""
        
        # Backend .env
        backend_env = """# Database
DATABASE_URL=postgresql://ishop_user:ishop_pass@localhost/ishop_db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-please-make-it-very-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379

# Email (Optional)
SMTP_TLS=True
SMTP_PORT=587
SMTP_HOST=smtp.gmail.com
SMTP_USER=
SMTP_PASSWORD=

# OAuth (Optional)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
TELEGRAM_BOT_TOKEN=
"""
        self.write_file("backend/.env.example", backend_env)
        self.write_file("backend/.env", backend_env)
        
        # Frontend .env
        frontend_env = """REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
REACT_APP_TELEGRAM_BOT_NAME=your-telegram-bot
"""
        self.write_file("frontend/.env.example", frontend_env)
        self.write_file("frontend/.env", frontend_env)
        
        print("✅ فایل‌های environment ایجاد شد")

    def write_file(self, path, content):
        """نوشتن محتوا در فایل"""
        file_path = self.base_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_project(self):
        """تولید کامل پروژه"""
        print("🎯 شروع تولید پروژه iShop...")
        print(f"📁 مسیر پروژه: {self.base_path.absolute()}")
        
        try:
            # ایجاد ساختار
            self.create_directory_structure()
            
            # ایجاد فایل‌های بک‌اند
            self.create_backend_files()
            
            # ایجاد فایل‌های فرانت‌اند
            self.create_frontend_files()
            
            # ایجاد فایل‌های Docker
            self.create_docker_files()
            
            # ایجاد اسکریپت‌های راه‌اندازی
            self.create_setup_scripts()
            
            # ایجاد فایل‌های environment
            self.create_env_files()
            
            # ایجاد README
            self.create_readme()
            
            print("\n🎉 پروژه با موفقیت ایجاد شد!")
            print(f"📁 مسیر: {self.base_path.absolute()}")
            print("\n🚀 برای شروع:")
            print(f"cd {self.project_name}")
            print("chmod +x scripts/setup.sh")
            print("./scripts/setup.sh")
            print("\n✨ سپس به آدرس http://localhost:3000 بروید")
            
        except Exception as e:
            print(f"❌ خطا در ایجاد پروژه: {e}")
            sys.exit(1)

def main():
    print("🛍️ iShop Project Generator")
    print("=" * 50)
    
    project_name = input("نام پروژه (پیش‌فرض: ishop): ").strip() or "ishop"
    
    generator = iShopGenerator(project_name)
    generator.generate_project()

if __name__ == "__main__":
    main()