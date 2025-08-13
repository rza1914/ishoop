# backend/telegram_bot/importer.py
import requests
import logging
from typing import List, Dict
from .config import API_BASE_URL

logger = logging.getLogger(__name__)

class ProductImporter:
    """کلاس برای ایمپورت محصولات از فایل‌های مختلف"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
        
    def save_products_to_api(self, products: List[Dict]) -> Dict:
        """
        ذخیره محصولات در API سایت
        
        Args:
            products: لیست محصولات
            
        Returns:
            Dict: نتیجه عملیات
        """
        try:
            success_count = 0
            failed_products = []
            
            for product in products:
                try:
                    # ارسال به API سایت
                    response = requests.post(
                        f"{self.api_base_url}/products/",
                        json=product,
                        timeout=30
                    )
                    
                    if response.status_code in [200, 201]:
                        success_count += 1
                    else:
                        failed_products.append({
                            'product': product.get('name', 'Unknown'),
                            'error': f"HTTP {response.status_code}"
                        })
                        
                except Exception as e:
                    failed_products.append({
                        'product': product.get('name', 'Unknown'),
                        'error': str(e)
                    })
            
            return {
                'success': True,
                'imported_count': success_count,
                'failed_count': len(failed_products),
                'failed_products': failed_products
            }
            
        except Exception as e:
            logger.error(f"Error saving products to API: {e}")
            return {
                'success': False,
                'error': str(e)
            }