# backend/telegram_bot/config.py
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_TELEGRAM_IDS = os.getenv("ADMIN_TELEGRAM_IDS", "").split(",")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
CURRENCY_RATE_ENDPOINT = f"{API_BASE_URL}/currency/rate"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB