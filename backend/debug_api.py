#!/usr/bin/env python3
"""
🔧 iShop API Debug Script
اسکریپت کامل برای تست و دیباگ API

استفاده:
    python debug_api.py
    python debug_api.py --detailed
    python debug_api.py --test-auth
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, Any, List

class Colors:
    """رنگ‌های ANSI برای terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class APIDebugger:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.test_user = {
            "email": "debug@ishop.com",
            "password": "debug123",
            "full_name": "Debug User"
        }
        self.auth_token = None
        
    def log(self, message: str, color: str = Colors.WHITE):
        """لاگ با رنگ"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.CYAN}[{timestamp}]{Colors.END} {color}{message}{Colors.END}")
    
    def success(self, message: str):
        """لاگ موفقیت"""
        self.log(f"✅ {message}", Colors.GREEN)
    
    def error(self, message: str):
        """لاگ خطا"""
        self.log(f"❌ {message}", Colors.RED)
    
    def warning(self, message: str):
        """لاگ هشدار"""
        self.log(f"⚠️ {message}", Colors.YELLOW)
    
    def info(self, message: str):
        """لاگ اطلاعات"""
        self.log(f"ℹ️ {message}", Colors.BLUE)
    
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, 
                     expected_status: int = 200, description: str = "") -> Dict[str, Any]:
        """تست یک endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            # نتیجه تست
            result = {
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": response.status_code == expected_status,
                "response_time": response.elapsed.total_seconds(),
                "description": description,
                "url": url
            }
            
            try:
                result["response_data"] = response.json()
            except:
                result["response_data"] = response.text
            
            # لاگ نتیجه
            if result["success"]:
                self.success(f"{method} {endpoint} - {description} ({response.status_code})")
            else:
                self.error(f"{method} {endpoint} - {description} (got {response.status_code}, expected {expected_status})")
            
            self.test_results.append(result)
            return result
            
        except requests.exceptions.ConnectionError:
            self.error(f"❌ نمی‌تونم به سرور وصل بشم! آیا سرور روی {self.base_url} اجرا می‌شه؟")
            return {"success": False, "error": "Connection failed"}
        except Exception as e:
            self.error(f"❌ خطا در تست {endpoint}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def test_server_health(self):
        """تست سلامت سرور"""
        self.info("🏥 تست سلامت سرور...")
        
        # تست root endpoint
        self.test_endpoint("GET", "/", description="Root endpoint")
        
        # تست health endpoint
        self.test_endpoint("GET", "/health", description="Health check")
        
        # تست debug endpoint
        self.test_endpoint("GET", "/debug", description="Debug data")
    
    def test_products(self):
        """تست endpoint های محصولات"""
        self.info("📦 تست محصولات...")
        
        # لیست محصولات
        products_result = self.test_endpoint("GET", "/api/v1/products/", description="Get all products")
        
        if products_result.get("success") and products_result.get("response_data"):
            products = products_result["response_data"]
            if isinstance(products, list) and len(products) > 0:
                self.success(f"✅ {len(products)} محصول یافت شد")
                
                # تست جزئیات یک محصول
                first_product_id = products[0].get("id")
                if first_product_id:
                    self.test_endpoint("GET", f"/api/v1/products/{first_product_id}", 
                                     description=f"Get product {first_product_id}")
                
                # نمایش نمونه محصول
                self.info(f"📱 نمونه محصول: {products[0].get('name', 'نامشخص')}")
            else:
                self.warning("⚠️ هیچ محصولی یافت نشد")
        
        # تست محصول ناموجود
        self.test_endpoint("GET", "/api/v1/products/999999", expected_status=200, 
                          description="Test non-existent product")
    
    def test_authentication(self):
        """تست authentication"""
        self.info("🔐 تست احراز هویت...")
        
        # تست ثبت‌نام
        register_result = self.test_endpoint("POST", "/api/v1/auth/register", 
                                           data=self.test_user, 
                                           description="User registration")
        
        if register_result.get("success"):
            self.success("✅ ثبت‌نام موفق")
            
            # تست ورود
            login_data = {
                "username": self.test_user["email"],
                "password": self.test_user["password"]
            }
            
            login_result = self.test_endpoint("POST", "/api/v1/auth/login", 
                                            data=login_data, 
                                            description="User login")
            
            if login_result.get("success") and login_result.get("response_data"):
                response_data = login_result["response_data"]
                if "access_token" in response_data:
                    self.auth_token = response_data["access_token"]
                    self.success("✅ ورود موفق - Token دریافت شد")
                    
                    # تنظیم header برای درخواست‌های بعدی
                    self.session.headers.update({
                        "Authorization": f"Bearer {self.auth_token}"
                    })
                else:
                    self.warning("⚠️ Token در پاسخ ورود یافت نشد")
        
        # تست اطلاعات کاربر
        self.test_endpoint("GET", "/api/v1/users/me", description="Get current user")
    
    def test_reviews(self):
        """تست نظرات"""
        self.info("⭐ تست نظرات...")
        
        # ایجاد نظر جدید
        review_data = {
            "product_id": 1,
            "rating": 5,
            "comment": "محصول عالی! توصیه می‌کنم."
        }
        
        self.test_endpoint("POST", "/api/v1/reviews/", data=review_data, 
                          description="Create review")
        
        # دریافت نظرات محصول
        self.test_endpoint("GET", "/api/v1/reviews/?product_id=1", 
                          description="Get product reviews")
        
        # دریافت تمام نظرات
        self.test_endpoint("GET", "/api/v1/reviews/", description="Get all reviews")
    
    def test_orders(self):
        """تست سفارشات"""
        self.info("🛒 تست سفارشات...")
        
        # ایجاد سفارش جدید
        order_data = {
            "items": [
                {"product_id": 1, "quantity": 2, "price": 45000000},
                {"product_id": 2, "quantity": 1, "price": 35000000}
            ],
            "total_amount": 125000000,
            "shipping_address": {
                "full_name": "کاربر تست",
                "address": "تهران، خیابان ولیعصر",
                "city": "تهران",
                "postal_code": "1234567890"
            }
        }
        
        self.test_endpoint("POST", "/api/v1/orders/", data=order_data, 
                          description="Create order")
        
        # دریافت سفارشات
        self.test_endpoint("GET", "/api/v1/orders/", description="Get orders")
    
    def test_performance(self):
        """تست عملکرد"""
        self.info("⚡ تست عملکرد...")
        
        start_time = time.time()
        
        # تست سرعت چندین درخواست
        for i in range(5):
            result = self.test_endpoint("GET", "/api/v1/products/", description=f"Performance test {i+1}")
            if not result.get("success"):
                break
        
        total_time = time.time() - start_time
        self.info(f"⏱️ زمان کل برای 5 درخواست: {total_time:.2f} ثانیه")
        
        # محاسبه میانگین زمان پاسخ
        response_times = [r.get("response_time", 0) for r in self.test_results if r.get("response_time")]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            self.info(f"📊 میانگین زمان پاسخ: {avg_time:.3f} ثانیه")
    
    def test_cors(self):
        """تست CORS"""
        self.info("🌐 تست CORS...")
        
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        try:
            response = self.session.options(f"{self.base_url}/api/v1/products/", headers=headers)
            if response.status_code == 200:
                self.success("✅ CORS پیکربندی شده")
            else:
                self.warning(f"⚠️ مشکل CORS - کد: {response.status_code}")
        except Exception as e:
            self.error(f"❌ خطا در تست CORS: {str(e)}")
    
    def generate_report(self):
        """تولید گزارش نهایی"""
        self.log("\n" + "="*50, Colors.BOLD)
        self.log("📊 گزارش نهایی تست API", Colors.BOLD)
        self.log("="*50, Colors.BOLD)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r.get("success")])
        failed_tests = total_tests - successful_tests
        
        self.info(f"📈 کل تست‌ها: {total_tests}")
        self.success(f"✅ موفق: {successful_tests}")
        if failed_tests > 0:
            self.error(f"❌ ناموفق: {failed_tests}")
        
        # نمایش تست‌های ناموفق
        if failed_tests > 0:
            self.warning("\n⚠️ تست‌های ناموفق:")
            for result in self.test_results:
                if not result.get("success"):
                    self.error(f"  • {result.get('method')} {result.get('endpoint')} - {result.get('description')}")
        
        # محاسبه نرخ موفقیت
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        if success_rate >= 90:
            self.success(f"🎉 نرخ موفقیت: {success_rate:.1f}% - عالی!")
        elif success_rate >= 70:
            self.warning(f"⚠️ نرخ موفقیت: {success_rate:.1f}% - قابل قبول")
        else:
            self.error(f"❌ نرخ موفقیت: {success_rate:.1f}% - نیاز به بررسی")
        
        # پیشنهادات
        self.log("\n💡 پیشنهادات:", Colors.MAGENTA)
        if self.auth_token:
            self.success("  • Authentication کار می‌کند")
        else:
            self.warning("  • Authentication را بررسی کنید")
        
        if successful_tests > 0:
            self.success("  • API در دسترس است")
        else:
            self.error("  • سرور را بررسی کنید")
        
        self.log("\n🚀 API آماده اتصال به Frontend!", Colors.GREEN)
    
    def run_all_tests(self, detailed: bool = False, test_auth: bool = True):
        """اجرای تمام تست‌ها"""
        self.log("🔧 شروع تست کامل iShop API", Colors.BOLD)
        self.log(f"🌐 Base URL: {self.base_url}", Colors.CYAN)
        self.log("-" * 50)
        
        try:
            # تست‌های اصلی
            self.test_server_health()
            self.test_products()
            
            if test_auth:
                self.test_authentication()
            
            self.test_reviews()
            self.test_orders()
            
            if detailed:
                self.test_performance()
                self.test_cors()
            
            # گزارش نهایی
            self.generate_report()
            
        except KeyboardInterrupt:
            self.warning("\n⚠️ تست توسط کاربر متوقف شد")
        except Exception as e:
            self.error(f"❌ خطای غیرمنتظره: {str(e)}")

def main():
    """تابع اصلی"""
    import argparse
    
    parser = argparse.ArgumentParser(description="🔧 iShop API Debug Tool")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--detailed", action="store_true", help="Run detailed tests including performance")
    parser.add_argument("--no-auth", action="store_true", help="Skip authentication tests")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    debugger = APIDebugger(args.url)
    debugger.run_all_tests(detailed=args.detailed, test_auth=not args.no_auth)
    
    if args.json:
        print("\n" + "="*30 + " JSON RESULTS " + "="*30)
        print(json.dumps(debugger.test_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()