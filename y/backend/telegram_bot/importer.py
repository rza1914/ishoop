# backend/telegram_bot/importer.py
import pandas as pd
import requests
import logging
from typing import List, Dict
from .config import API_BASE_URL
from .currency import currency_converter

logger = logging.getLogger(__name__)

class ProductImporter:
    """کلاس برای ایمپورت محصولات از فایل‌های مختلف"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
        
    def import_from_excel(self, file_path: str) -> List[Dict]:
        """
        ایمپورت محصولات از فایل Excel
        
        Args:
            file_path: مسیر فایل Excel
            
        Returns:
            List[Dict]: لیست محصولات
        """
        try:
            # خواندن فایل Excel
            df = pd.read_excel(file_path)
            return self._process_dataframe(df)
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            raise Exception(f"خطا در خواندن فایل Excel: {str(e)}")
    
    def import_from_csv(self, file_path: str) -> List[Dict]:
        """
        ایمپورت محصولات از فایل CSV
        
        Args:
            file_path: مسیر فایل CSV
            
        Returns:
            List[Dict]: لیست محصولات
        """
        try:
            # خواندن فایل CSV
            df = pd.read_csv(file_path, encoding='utf-8')
            return self._process_dataframe(df)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise Exception(f"خطا در خواندن فایل CSV: {str(e)}")
    
    def _process_dataframe(self, df: pd.DataFrame) -> List[Dict]:
        """
        پردازش DataFrame و تبدیل به لیست محصولات
        
        Args:
            df: DataFrame pandas
            
        Returns:
            List[Dict]: لیست محصولات
        """
        products = []
        required_columns = ['name', 'price']
        
        # بررسی وجود ستون‌های اجباری
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise Exception(f"ستون‌های اجباری موجود نیست: {', '.join(missing_columns)}")
        
        for index, row in df.iterrows():
            try:
                product = {
                    'name': str(row['name']).strip(),
                    'price': float(row['price']),
                    'description': str(row.get('description', '')).strip(),
                    'category': str(row.get('category', 'عمومی')).strip(),
                    'imageUrl': str(row.get('image_url', '')).strip()
                }
                
                # اعتبارسنجی
                if not product['name'] or product['price'] <= 0:
                    logger.warning(f"Row {index + 1}: Invalid product data")
                    continue
                
                # تبدیل ارز اگر نیاز باشد
                if row.get('currency', '').upper() == 'AED':
                    product['price'] = currency_converter.convert_aed_to_toman(product['price'])
                
                products.append(product)
                
            except Exception as e:
                logger.error(f"Error processing row {index + 1}: {e}")
                continue
        
        return products
        
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
                        f"{self.api_base_url}/products/create",
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