#!/usr/bin/env python3
"""
👑 iShop Admin Panel Debug Script
اسکریپت کامل برای تست تمام قابلیت‌های Admin Panel

استفاده:
    python admin_debug.py
    python admin_debug.py --detailed
    python admin_debug.py --create-sample-data
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

class AdminDebugger:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
        # Admin credentials
        self.admin_user = {
            "email": "admin@ishop.com",
            "password": "admin123",
            "full_name": "Admin User"
        }
        
        # Test data
        self.test_product = {
            "name": "محصول تست ادمین",
            "description": "این محصول برای تست admin panel ساخته شده",
            "price": 1000000,
            "category": "تست",
            "stock_quantity": 50,
            "image_url": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=400"
        }
        
        self.admin_token = None
        self.created_product_id = None
        
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

    def admin_info(self, message: str):
        """لاگ مخصوص admin"""
        self.log(f"👑 {message}", Colors.MAGENTA)
    
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, 
                     expected_status: int = 200, description: str = "", 
                     auth_required: bool = False) -> Dict[str, Any]:
        """تست یک endpoint"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        # Add auth header if required
        if auth_required and self.admin_token:
            headers['Authorization'] = f"Bearer {self.admin_token}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = self.session.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
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
                if result.get("response_data"):
                    self.error(f"   Response: {result['response_data']}")
            
            self.test_results.append(result)
            return result
            
        except requests.exceptions.ConnectionError:
            self.error(f"❌ نمی‌تونم به سرور وصل بشم! آیا سرور روی {self.base_url} اجرا می‌شه؟")
            return {"success": False, "error": "Connection failed"}
        except Exception as e:
            self.error(f"❌ خطا در تست {endpoint}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def setup_admin_auth(self):
        """راه‌اندازی احراز هویت admin"""
        self.admin_info("🔑 راه‌اندازی Admin Authentication...")
        
        # ثبت admin اگر وجود نداره
        register_result = self.test_endpoint("POST", "/api/v1/auth/register", 
                                           data=self.admin_user, 
                                           description="Admin registration",
                                           expected_status=200)
        
        # لاگین admin
        login_data = {
            "username": self.admin_user["email"],
            "password": self.admin_user["password"]
        }
        
        login_result = self.test_endpoint("POST", "/api/v1/auth/login", 
                                        data=login_data, 
                                        description="Admin login")
        
        if login_result.get("success") and login_result.get("response_data"):
            response_data = login_result["response_data"]
            if "access_token" in response_data:
                self.admin_token = response_data["access_token"]
                self.session.headers.update({
                    "Authorization": f"Bearer {self.admin_token}"
                })
                self.success("✅ Admin Token دریافت شد")
                return True
        
        self.error("❌ Admin Authentication ناموفق")
        return False
    
    def test_admin_dashboard(self):
        """تست Dashboard ادمین"""
        self.admin_info("📊 تست Admin Dashboard...")
        
        # تست دسترسی به صفحه admin
        self.test_endpoint("GET", "/admin", description="Admin dashboard access")
        
        # تست آمار کلی
        self.test_endpoint("GET", "/api/v1/admin/stats", 
                          description="Admin statistics", 
                          auth_required=True)
        
        # تست dashboard data
        self.test_endpoint("GET", "/api/v1/admin/dashboard", 
                          description="Dashboard data", 
                          auth_required=True)
        
        # تست گزارشات
        self.test_endpoint("GET", "/api/v1/admin/reports", 
                          description="Admin reports", 
                          auth_required=True)
    
    def test_product_management(self):
        """تست مدیریت محصولات"""
        self.admin_info("📦 تست Product Management...")
        
        # CREATE - ایجاد محصول جدید
        create_result = self.test_endpoint("POST", "/api/v1/admin/products", 
                                         data=self.test_product, 
                                         description="Create new product",
                                         auth_required=True)
        
        if create_result.get("success") and create_result.get("response_data"):
            self.created_product_id = create_result["response_data"].get("id")
            self.success(f"✅ محصول جدید ایجاد شد (ID: {self.created_product_id})")
        
        # READ - دریافت لیست محصولات admin
        self.test_endpoint("GET", "/api/v1/admin/products", 
                          description="Get all products (admin view)", 
                          auth_required=True)
        
        # READ - جزئیات محصول برای admin
        if self.created_product_id:
            self.test_endpoint("GET", f"/api/v1/admin/products/{self.created_product_id}", 
                              description=f"Get product details (admin)", 
                              auth_required=True)
        
        # UPDATE - ویرایش محصول
        if self.created_product_id:
            updated_product = self.test_product.copy()
            updated_product["name"] = "محصول تست ادمین (ویرایش شده)"
            updated_product["price"] = 1200000
            
            self.test_endpoint("PUT", f"/api/v1/admin/products/{self.created_product_id}", 
                              data=updated_product,
                              description="Update product", 
                              auth_required=True)
        
        # تست inventory management
        if self.created_product_id:
            inventory_data = {"stock_quantity": 100}
            self.test_endpoint("PATCH", f"/api/v1/admin/products/{self.created_product_id}/inventory", 
                              data=inventory_data,
                              description="Update product inventory", 
                              auth_required=True)
    
    def test_user_management(self):
        """تست مدیریت کاربران"""
        self.admin_info("👥 تست User Management...")
        
        # دریافت لیست کاربران
        self.test_endpoint("GET", "/api/v1/admin/users", 
                          description="Get all users", 
                          auth_required=True)
        
        # جستجو کاربران
        self.test_endpoint("GET", "/api/v1/admin/users?search=admin", 
                          description="Search users", 
                          auth_required=True)
        
        # آمار کاربران
        self.test_endpoint("GET", "/api/v1/admin/users/stats", 
                          description="User statistics", 
                          auth_required=True)
        
        # تست مدیریت نقش‌ها (اگر موجود باشه)
        self.test_endpoint("GET", "/api/v1/admin/roles", 
                          description="Get user roles", 
                          auth_required=True)
    
    def test_order_management(self):
        """تست مدیریت سفارشات"""
        self.admin_info("🛒 تست Order Management...")
        
        # دریافت تمام سفارشات
        self.test_endpoint("GET", "/api/v1/admin/orders", 
                          description="Get all orders", 
                          auth_required=True)
        
        # فیلتر سفارشات بر اساس وضعیت
        self.test_endpoint("GET", "/api/v1/admin/orders?status=pending", 
                          description="Get pending orders", 
                          auth_required=True)
        
        # آمار سفارشات
        self.test_endpoint("GET", "/api/v1/admin/orders/stats", 
                          description="Order statistics", 
                          auth_required=True)
        
        # گزارش فروش
        self.test_endpoint("GET", "/api/v1/admin/sales/report", 
                          description="Sales report", 
                          auth_required=True)
    
    def test_analytics(self):
        """تست Analytics و گزارشات"""
        self.admin_info("📈 تست Analytics...")
        
        # آمار کلی سایت
        self.test_endpoint("GET", "/api/v1/admin/analytics/overview", 
                          description="Site analytics overview", 
                          auth_required=True)
        
        # گزارش فروش ماهانه
        self.test_endpoint("GET", "/api/v1/admin/analytics/sales-monthly", 
                          description="Monthly sales report", 
                          auth_required=True)
        
        # محبوب‌ترین محصولات
        self.test_endpoint("GET", "/api/v1/admin/analytics/popular-products", 
                          description="Popular products", 
                          auth_required=True)
        
        # آمار کاربران فعال
        self.test_endpoint("GET", "/api/v1/admin/analytics/active-users", 
                          description="Active users analytics", 
                          auth_required=True)
    
    def test_settings(self):
        """تست تنظیمات سایت"""
        self.admin_info("⚙️ تست Site Settings...")
        
        # دریافت تنظیمات فعلی
        self.test_endpoint("GET", "/api/v1/admin/settings", 
                          description="Get site settings", 
                          auth_required=True)
        
        # به‌روزرسانی تنظیمات
        settings_data = {
            "site_name": "iShop Admin Test",
            "maintenance_mode": False,
            "allow_registration": True
        }
        
        self.test_endpoint("PUT", "/api/v1/admin/settings", 
                          data=settings_data,
                          description="Update site settings", 
                          auth_required=True)
        
        # تست backup database
        self.test_endpoint("POST", "/api/v1/admin/backup", 
                          description="Create database backup", 
                          auth_required=True)
    
    def test_content_management(self):
        """تست مدیریت محتوا"""
        self.admin_info("📝 تست Content Management...")
        
        # مدیریت دسته‌بندی‌ها
        category_data = {
            "name": "دسته تست",
            "description": "دسته‌بندی برای تست admin panel"
        }
        
        self.test_endpoint("POST", "/api/v1/admin/categories", 
                          data=category_data,
                          description="Create new category", 
                          auth_required=True)
        
        # دریافت دسته‌بندی‌ها
        self.test_endpoint("GET", "/api/v1/admin/categories", 
                          description="Get all categories", 
                          auth_required=True)
        
        # مدیریت برندها (اگر موجود باشه)
        self.test_endpoint("GET", "/api/v1/admin/brands", 
                          description="Get all brands", 
                          auth_required=True)
    
    def test_security_features(self):
        """تست ویژگی‌های امنیتی"""
        self.admin_info("🔒 تست Security Features...")
        
        # لاگ فعالیت‌های admin
        self.test_endpoint("GET", "/api/v1/admin/activity-logs", 
                          description="Admin activity logs", 
                          auth_required=True)
        
        # تست تلاش‌های ورود ناموفق
        self.test_endpoint("GET", "/api/v1/admin/failed-logins", 
                          description="Failed login attempts", 
                          auth_required=True)
        
        # آمار امنیتی
        self.test_endpoint("GET", "/api/v1/admin/security/stats", 
                          description="Security statistics", 
                          auth_required=True)
    
    def cleanup_test_data(self):
        """پاکسازی داده‌های تست"""
        self.admin_info("🧹 پاکسازی Test Data...")
        
        # حذف محصول تست
        if self.created_product_id:
            self.test_endpoint("DELETE", f"/api/v1/admin/products/{self.created_product_id}", 
                              description="Delete test product", 
                              auth_required=True)
    
    def create_sample_data(self):
        """ایجاد داده‌های نمونه برای تست"""
        self.admin_info("📋 ایجاد Sample Data...")
        
        sample_products = [
            {
                "name": "گوشی Samsung Galaxy S24 Ultra",
                "description": "جدیدترین گوشی سامسونگ با قابلیت‌های پیشرفته",
                "price": 55000000,
                "category": "موبایل",
                "stock_quantity": 25,
                "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"
            },
            {
                "name": "لپ‌تاپ Dell XPS 13",
                "description": "لپ‌تاپ فوق‌العاده سبک و قدرتمند",
                "price": 45000000,
                "category": "لپ‌تاپ",
                "stock_quantity": 15,
                "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"
            },
            {
                "name": "هدست Gaming Razer",
                "description": "هدست گیمینگ با کیفیت صدای فوق‌العاده",
                "price": 3500000,
                "category": "گیمینگ",
                "stock_quantity": 40,
                "image_url": "https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400"
            }
        ]
        
        for product in sample_products:
            self.test_endpoint("POST", "/api/v1/admin/products", 
                              data=product,
                              description=f"Create sample product: {product['name'][:20]}...", 
                              auth_required=True)
    
    def generate_admin_report(self):
        """تولید گزارش نهایی Admin"""
        self.log("\n" + "="*60, Colors.BOLD)
        self.log("👑 گزارش نهایی تست Admin Panel", Colors.BOLD)
        self.log("="*60, Colors.BOLD)
        
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if r.get("success")])
        failed_tests = total_tests - successful_tests
        
        self.info(f"📈 کل تست‌های Admin: {total_tests}")
        self.success(f"✅ موفق: {successful_tests}")
        if failed_tests > 0:
            self.error(f"❌ ناموفق: {failed_tests}")
        
        # دسته‌بندی تست‌ها
        admin_categories = {
            "Authentication": ["login", "register", "auth"],
            "Dashboard": ["dashboard", "stats", "reports"],
            "Products": ["products", "inventory"],
            "Users": ["users", "roles"],
            "Orders": ["orders", "sales"],
            "Analytics": ["analytics", "overview"],
            "Settings": ["settings", "backup"],
            "Content": ["categories", "brands"],
            "Security": ["activity", "failed", "security"]
        }
        
        self.log("\n📊 نتایج بر اساس دسته‌بندی:", Colors.CYAN)
        
        for category, keywords in admin_categories.items():
            category_tests = [r for r in self.test_results 
                            if any(keyword in r.get("endpoint", "").lower() 
                                  for keyword in keywords)]
            
            if category_tests:
                successful = len([t for t in category_tests if t.get("success")])
                total = len(category_tests)
                percentage = (successful / total * 100) if total > 0 else 0
                
                if percentage == 100:
                    self.success(f"  👑 {category}: {successful}/{total} ({percentage:.0f}%)")
                elif percentage >= 80:
                    self.warning(f"  ⚠️ {category}: {successful}/{total} ({percentage:.0f}%)")
                else:
                    self.error(f"  ❌ {category}: {successful}/{total} ({percentage:.0f}%)")
        
        # محاسبه نرخ موفقیت کلی
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        self.log("\n🎯 ارزیابی کلی Admin Panel:", Colors.MAGENTA)
        
        if success_rate >= 95:
            self.success(f"🏆 نرخ موفقیت: {success_rate:.1f}% - Admin Panel فوق‌العاده!")
        elif success_rate >= 85:
            self.success(f"✅ نرخ موفقیت: {success_rate:.1f}% - Admin Panel عالی!")
        elif success_rate >= 70:
            self.warning(f"⚠️ نرخ موفقیت: {success_rate:.1f}% - Admin Panel قابل قبول")
        else:
            self.error(f"❌ نرخ موفقیت: {success_rate:.1f}% - Admin Panel نیاز به بررسی")
        
        # پیشنهادات مخصوص Admin
        self.log("\n💡 پیشنهادات Admin Panel:", Colors.MAGENTA)
        
        if self.admin_token:
            self.success("  • Admin Authentication کار می‌کند")
        else:
            self.error("  • Admin Authentication را بررسی کنید")
        
        if successful_tests > total_tests * 0.8:
            self.success("  • Admin Panel آماده production است")
        else:
            self.warning("  • Admin Panel نیاز به بهبود دارد")
        
        # Admin-specific recommendations
        self.log("\n🚀 توصیه‌های Admin Panel:", Colors.BLUE)
        self.info("  • Dashboard metrics را بهبود دهید")
        self.info("  • User role management اضافه کنید") 
        self.info("  • Advanced analytics پیاده‌سازی کنید")
        self.info("  • Security monitoring تقویت کنید")
        self.info("  • Bulk operations اضافه کنید")
        
        self.log("\n👑 Admin Panel آماده مدیریت حرفه‌ای!", Colors.GREEN)
    
    def run_admin_tests(self, detailed: bool = False, create_data: bool = False):
        """اجرای تمام تست‌های Admin"""
        self.log("👑 شروع تست کامل Admin Panel", Colors.BOLD)
        self.log(f"🌐 Base URL: {self.base_url}", Colors.CYAN)
        self.log("-" * 60)
        
        try:
            # راه‌اندازی Auth
            if not self.setup_admin_auth():
                self.error("❌ Admin Authentication ناموفق - متوقف می‌شویم")
                return
            
            # ایجاد داده‌های نمونه
            if create_data:
                self.create_sample_data()
            
            # تست‌های اصلی Admin
            self.test_admin_dashboard()
            self.test_product_management()
            self.test_user_management()
            self.test_order_management()
            
            if detailed:
                self.test_analytics()
                self.test_settings()
                self.test_content_management()
                self.test_security_features()
            
            # پاکسازی
            if not create_data:  # فقط اگر داده‌های نمونه نساختیم
                self.cleanup_test_data()
            
            # گزارش نهایی
            self.generate_admin_report()
            
        except KeyboardInterrupt:
            self.warning("\n⚠️ تست Admin توسط کاربر متوقف شد")
        except Exception as e:
            self.error(f"❌ خطای غیرمنتظره در Admin tests: {str(e)}")

def main():
    """تابع اصلی"""
    import argparse
    
    parser = argparse.ArgumentParser(description="👑 iShop Admin Panel Debug Tool")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--detailed", action="store_true", help="Run detailed admin tests")
    parser.add_argument("--create-sample-data", action="store_true", help="Create sample data for testing")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    
    args = parser.parse_args()
    
    debugger = AdminDebugger(args.url)
    debugger.run_admin_tests(
        detailed=args.detailed, 
        create_data=args.create_sample_data
    )
    
    if args.json:
        print("\n" + "="*30 + " JSON RESULTS " + "="*30)
        print(json.dumps(debugger.test_results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()