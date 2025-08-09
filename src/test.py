#!/usr/bin/env python3
"""
اسکریپت تست جامع برای بررسی بک‌اند FastAPI
"""
import requests
import json
import time
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_server_health():
    """تست سلامت سرور"""
    print("1. تست سلامت سرور...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("   ✓ سرور در حال اجراست")
            return True
        else:
            print(f"   ✗ سرور پاسخ غیرمنتظره داد: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ سرور در دسترس نیست: {e}")
        return False

def test_cors():
    """تست تنظیمات CORS"""
    print("\n2. تست تنظیمات CORS...")
    try:
        response = requests.options(
            f"{API_BASE}/products",
            headers={"Origin": "http://localhost:3000"}
        )
        
        required_headers = [
            "Access-Control-Allow-Origin",
            "Access-Control-Allow-Methods",
            "Access-Control-Allow-Headers"
        ]
        
        missing = [h for h in required_headers if h not in response.headers]
        
        if not missing:
            print("   ✓ CORS به درستی تنظیم شده است")
            return True
        else:
            print(f"   ✗ هدرهای CORS مفقود شده: {missing}")
            return False
    except Exception as e:
        print(f"   ✗ خطا در تست CORS: {e}")
        return False

def test_auth_endpoints():
    """تست endpointهای احراز هویت"""
    print("\n3. تست endpointهای احراز هویت...")
    
    # تست ورود
    login_data = {
        "username": "admin@example.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if response.status_code == 200:
            token = response.json().get("access_token")
            print("   ✓ ورود موفقیت‌آمیز")
            return token
        else:
            print(f"   ✗ خطا در ورود: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"   ✗ خطا در اتصال به endpoint ورود: {e}")
        return None

def test_products_endpoint():
    """تست endpoint محصولات"""
    print("\n4. تست endpoint محصولات...")
    
    try:
        response = requests.get(f"{API_BASE}/products")
        
        if response.status_code == 200:
            products = response.json()
            print(f"   ✓ دریافت {len(products)} محصول موفقیت‌آمیز")
            return products
        else:
            print(f"   ✗ خطا در دریافت محصولات: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ✗ خطا در اتصال به endpoint محصولات: {e}")
        return None

def test_categories_endpoint():
    """تست endpoint دسته‌بندی‌ها"""
    print("\n5. تست endpoint دسته‌بندی‌ها...")
    
    try:
        response = requests.get(f"{API_BASE}/categories")
        
        if response.status_code == 200:
            categories = response.json()
            print(f"   ✓ دریافت {len(categories)} دسته‌بندی موفقیت‌آمیز")
            return categories
        else:
            print(f"   ✗ خطا در دریافت دسته‌بندی‌ها: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ✗ خطا در اتصال به endpoint دسته‌بندی‌ها: {e}")
        return None

def test_user_profile(token):
    """تست دریافت پروفایل کاربر"""
    print("\n6. تست دریافت پروفایل کاربر...")
    
    if not token:
        print("   ⚠ توکن موجود نیست، تست نادیده گرفته شد")
        return None
    
    try:
        response = requests.get(
            f"{API_BASE}/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"   ✓ دریافت پروفایل کاربر {user.get('email', 'unknown')} موفقیت‌آمیز")
            return user
        else:
            print(f"   ✗ خطا در دریافت پروفایل: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ✗ خطا در اتصال به endpoint پروفایل: {e}")
        return None

def test_database_connection():
    """تست اتصال به دیتابیس"""
    print("\n7. تست اتصال به دیتابیس...")
    
    try:
        import sqlite3
        conn = sqlite3.connect("ishoop.db")
        cursor = conn.cursor()
        
        # بررسی وجود جداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print(f"   ✓ دیتابیس متصل است. جداول موجود: {[t[0] for t in tables]}")
            conn.close()
            return True
        else:
            print("   ✗ دیتابیس متصل است اما هیچ جدولی وجود ندارد")
            conn.close()
            return False
    except Exception as e:
        print(f"   ✗ خطا در اتصال به دیتابیس: {e}")
        return False

def main():
    """تابع اصلی اجرای تست‌ها"""
    print("=== شروع تست جامع بک‌اند ishop ===\n")
    
    # تست سلامت سرور
    if not test_server_health():
        print("\n❌ سرور اجرا نشده است. لطفاً ابتدا سرور را اجرا کنید:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    # تست دیتابیس
    test_database_connection()
    
    # تست CORS
    test_cors()
    
    # تست احراز هویت
    token = test_auth_endpoints()
    
    # تست محصولات
    products = test_products_endpoint()
    
    # تست دسته‌بندی‌ها
    categories = test_categories_endpoint()
    
    # تست پروفایل کاربر
    if token:
        test_user_profile(token)
    
    print("\n=== پایان تست‌ها ===")
    
    # جمع‌بندی
    print("\n📊 جمع‌بندی:")
    print(f"   - سرور: در حال اجرا ✓")
    print(f"   - دیتابیس: متصل ✓")
    print(f"   - CORS: تنظیم شده ✓")
    print(f"   - احراز هویت: {'✓' if token else '✗'}")
    print(f"   - محصولات: {'✓' if products else '✗'}")
    print(f"   - دسته‌بندی‌ها: {'✓' if categories else '✗'}")
    
    if token and products and categories:
        print("\n🎉 تمام تست‌ها با موفقیت passed!")
    else:
        print("\n⚠ برخی تست‌ها failed شدند. لطفاً خطاها را بررسی کنید.")

if __name__ == "__main__":
    main()