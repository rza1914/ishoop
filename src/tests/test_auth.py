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

def test_send_otp():
    response = client.post('/api/v1/auth/send-otp', json={'phone': '09123456789'})
    assert response.status_code == 200
    assert 'otp' in response.json()

def test_verify_otp():
    # ابتدا OTP ارسال می‌کنیم
    client.post('/api/v1/auth/send-otp', json={'phone': '09123456789'})
    
    # سپس OTP را تأیید می‌کنیم
    response = client.post('/api/v1/auth/verify-otp', json={
        'phone': '09123456789',
        'otp': '123456'  # در تست واقعی، OTP ارسال شده را استفاده کنید
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_protected_route():
    # ابتدا احراز هویت می‌کنیم
    client.post('/api/v1/auth/send-otp', json={'phone': '09123456789'})
    auth_response = client.post('/api/v1/auth/verify-otp', json={
        'phone': '09123456789',
        'otp': '123456'
    })
    token = auth_response.json()['access_token']
    
    # سپس یک مسیر محافظت شده را صدا می‌زنیم
    response = client.get(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json()['phone'] == '09123456789'
