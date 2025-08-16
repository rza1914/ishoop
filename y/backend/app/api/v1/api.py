from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth_new as auth,
    users,
    products,
    orders,
    reviews,
    blog,
    currency
)

api_router = APIRouter()

# Authentication routes
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

# User routes
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

# Product routes
api_router.include_router(
    products.router,
    prefix="/products",
    tags=["products"]
)

# Order routes
api_router.include_router(
    orders.router,
    prefix="/orders",
    tags=["orders"]
)

# Review routes
api_router.include_router(
    reviews.router,
    prefix="/reviews",
    tags=["reviews"]
)

# Blog routes
api_router.include_router(
    blog.router,
    prefix="/blog",
    tags=["blog"]
)

# Currency routes
api_router.include_router(
    currency.router,
    prefix="/currency",
    tags=["currency"]
)