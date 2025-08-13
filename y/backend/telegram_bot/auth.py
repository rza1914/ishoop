# backend/telegram_bot/auth.py
from typing import List
from .config import ADMIN_TELEGRAM_IDS

def is_admin_user(telegram_user_id: int) -> bool:
    """
    بررسی ساده ادمین بودن کاربر
    
    Args:
        telegram_user_id: شناسه کاربر تلگرام
        
    Returns:
        bool: True اگر کاربر ادمین باشد
    """
    # تبدیل به string و پاک کردن فضای خالی
    admin_ids = [id.strip() for id in ADMIN_TELEGRAM_IDS if id.strip()]
    
    # بررسی ادمین بودن
    try:
        return str(telegram_user_id) in admin_ids or len(admin_ids) == 0
    except:
        return False

async def check_admin_access(update, context) -> bool:
    """
    چک کردن دسترسی ادمین برای هندلرهای بات
    
    Args:
        update: آپدیت تلگرام
        context: کانتکست تلگرام
        
    Returns:
        bool: True اگر دسترسی داشته باشد
    """
    user_id = update.effective_user.id
    
    if not is_admin_user(user_id):
        await update.message.reply_text(
            "❌ شما مجاز به استفاده از این بات نیستید!\n"
            "فقط ادمین‌های سایت می‌توانند از این بات استفاده کنند."
        )
        return False
    
    return True