# backend/telegram_bot/currency.py
import requests
from .config import CURRENCY_RATE_ENDPOINT

class CurrencyConverter:
    """کلاس برای تبدیل نرخ ارز"""
    
    @staticmethod
    def get_aed_to_toman_rate():
        """
        دریافت نرخ درهم به تومان از API سایت
        """
        try:
            response = requests.get(CURRENCY_RATE_ENDPOINT, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return float(data.get('rate', 11000.0))
        except Exception as e:
            print(f"Error fetching currency rate: {e}")
            # نرخ پیش‌فرض
            return 11000.0
    
    @staticmethod
    def convert_aed_to_toman(aed_amount: float) -> float:
        """
        تبدیل مبلغ درهم به تومان
        """
        rate = CurrencyConverter.get_aed_to_toman_rate()
        return round(aed_amount * rate, 0)

# ایجاد instance
currency_converter = CurrencyConverter()