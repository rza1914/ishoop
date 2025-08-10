from pydantic import BaseModel
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
