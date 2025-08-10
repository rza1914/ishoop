import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_product():
    return {
        'name': 'Test Product',
        'description': 'A test product',
        'price': 99.99,
        'stock': 10,
        'category': 'test'
    }

def test_create_product(test_product):
    response = client.post('/api/v1/products/', json=test_product)
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == test_product['name']
    assert data['price'] == test_product['price']

def test_get_products():
    response = client.get('/api/v1/products/')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product():
    # ابتدا یک محصول ایجاد می‌کنیم
    product_data = {
        'name': 'Test Product 2',
        'description': 'Another test product',
        'price': 149.99,
        'stock': 5,
        'category': 'test'
    }
    create_response = client.post('/api/v1/products/', json=product_data)
    product_id = create_response.json()['id']
    
    # سپس محصول را دریافت می‌کنیم
    response = client.get(f'/api/v1/products/{product_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == product_data['name']

def test_search_products():
    # ایجاد چند محصول برای جستجو
    products = [
        {'name': 'Laptop', 'description': 'A powerful laptop', 'price': 999.99, 'stock': 5, 'category': 'electronics'},
        {'name': 'Phone', 'description': 'A smartphone', 'price': 699.99, 'stock': 10, 'category': 'electronics'},
        {'name': 'Book', 'description': 'A good book', 'price': 19.99, 'stock': 20, 'category': 'books'}
    ]
    
    for product in products:
        client.post('/api/v1/products/', json=product)
    
    # جستجوی محصولات الکترونیکی
    response = client.get('/api/v1/products/?search=electronics')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(product['category'] == 'electronics' for product in data)
