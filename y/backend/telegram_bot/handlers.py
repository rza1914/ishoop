# backend/telegram_bot/handlers.py
import os
import logging
import re
from telegram import Update, PhotoSize
from telegram.ext import ContextTypes
from .auth import check_admin_access
from .importer import ProductImporter
from .config import MAX_FILE_SIZE
from .currency import currency_converter

logger = logging.getLogger(__name__)
importer = ProductImporter()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /start - شروع بات"""
    if not await check_admin_access(update, context):
        return
        
    welcome_message = """
🤖 به بات ایمپورت محصولات خوش آمدید!
    
دستورات موجود:
📥 /upload - آپلود فایل Excel یا CSV
❓ /help - راهنمای استفاده
⚙️ /status - وضعیت بات
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /help - راهنمای استفاده"""
    if not await check_admin_access(update, context):
        return
        
    help_text = """
📥 نحوه ایمپورت محصولات:
    
1️⃣ فایل Excel یا CSV خود را آپلود کنید
2️⃣ فایل باید شامل ستون‌های زیر باشد:

📋 ساختار فایل:
| name | description | price | category | image_url | stock |
|------|-------------|-------|----------|-----------|-------|
| محصول ۱ | توضیحات... | 10000 | الکترونیک | http://... | 10 |

✅ نکات مهم:
• حداکثر حجم فایل: 10MB
• فرمت‌های پشتیبانی شده: Excel (.xlsx) و CSV
• ستون‌های name و price اجباری هستند
• قیمت باید به عدد باشد
    """
    await update.message.reply_text(help_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور /status - نمایش وضعیت"""
    if not await check_admin_access(update, context):
        return
        
    # دریافت نرخ فعلی
    current_rate = currency_converter.get_aed_to_toman_rate()
    
    status_text = f"""
📊 وضعیت بات ایمپورت محصولات

✅ در حال کار
🔗 متصل به API سایت
💱 نرخ تبدیل: {current_rate:,.0f} تومان برای هر درهم
📥 آماده دریافت فایل‌های Excel/CSV

برای شروع، فایل خود را آپلود کنید.
    """
    await update.message.reply_text(status_text)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندل کردن فایل‌های آپلود شده"""
    # چک کردن دسترسی ادمین
    if not await check_admin_access(update, context):
        return
    
    try:
        document = update.message.document
        
        # بررسی وجود فایل
        if not document:
            await update.message.reply_text("❌ لطفاً یک فایل آپلود کنید!")
            return
            
        # بررسی حجم فایل
        if document.file_size > MAX_FILE_SIZE:
            await update.message.reply_text("❌ حجم فایل بیش از حد مجاز است! (حداکثر 10MB)")
            return
            
        # بررسی فرمت فایل
        allowed_mime_types = [
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/csv',
            'application/csv'
        ]
        
        if document.mime_type not in allowed_mime_types and not document.file_name.endswith(('.xlsx', '.xls', '.csv')):
            await update.message.reply_text("❌ لطفاً فایل Excel یا CSV آپلود کنید!")
            return
            
        # اطلاع‌رسانی شروع پردازش
        processing_message = await update.message.reply_text("🔄 در حال دریافت و پردازش فایل...")
        
        # دانلود فایل
        file = await context.bot.get_file(document.file_id)
        file_extension = os.path.splitext(document.file_name)[1].lower()
        temp_file_path = f"temp_import_{update.effective_user.id}{file_extension}"
        
        await file.download_to_drive(temp_file_path)
        
        # به‌روزرسانی پیام
        await processing_message.edit_text("🔍 در حال تحلیل فایل...")
        
        # پردازش فایل
        if file_extension in ['.csv']:
            products = importer.import_from_csv(temp_file_path)
        else:
            products = importer.import_from_excel(temp_file_path)
            
        # به‌روزرسانی پیام
        await processing_message.edit_text(f"💾 در حال ذخیره {len(products)} محصول...")
        
        # ذخیره در API
        result = importer.save_products_to_api(products)
        
        # حذف فایل موقت
        try:
            os.remove(temp_file_path)
        except:
            pass
            
        # نمایش نتیجه
        if result.get('success'):
            success_count = result.get('imported_count', 0)
            failed_count = result.get('failed_count', 0)
            
            if failed_count == 0:
                result_message = f"✅ {success_count} محصول با موفقیت ایمپورت شد!"
            else:
                result_message = f"""
✅ {success_count} محصول ایمپورت شد
❌ {failed_count} محصول با خطا مواجه شد

جزئیات:
"""
                # اضافه کردن جزئیات خطاها
                failed_products = result.get('failed_products', [])[:5]  # فقط 5 مورد اول
                for failed in failed_products:
                    result_message += f"• {failed['product']}: {failed['error']}\n"
                    
                if len(result.get('failed_products', [])) > 5:
                    result_message += f"\nو {len(result.get('failed_products', [])) - 5} مورد دیگر..."
        else:
            result_message = f"❌ خطا در ایمپورت محصولات:\n{result.get('error', 'خطای نامشخص')}"
            
        await processing_message.edit_text(result_message)
        
    except Exception as e:
        logger.error(f"Error handling document: {e}")
        await update.message.reply_text(f"❌ خطا در پردازش فایل:\n{str(e)}")