# backend/telegram_bot/bot.py
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from .handlers import start_command, help_command, status_command, handle_document
from .config import TELEGRAM_BOT_TOKEN

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def create_bot():
    """ایجاد و پیکربندی بات"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables!")
    
    # ایجاد اپلیکیشن
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # هندلر فایل‌ها
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    return application

async def main():
    """تابع اصلی بات"""
    try:
        # ایجاد بات
        application = create_bot()
        
        # شروع بات
        print("🤖 بات تلگرام ایمپورت محصولات در حال اجراست...")
        print("برای توقف از Ctrl+C استفاده کنید.")
        
        await application.run_polling()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        print(f"❌ خطا در اجرای بات: {e}")

if __name__ == "__main__":
    # اجرای بات
    asyncio.run(main())