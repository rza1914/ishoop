# backend/telegram_bot/config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # برای محدود کردن دسترسی
API_BASE_URL = "http://localhost:8000/api/v1"  # آدرس API بک‌اند