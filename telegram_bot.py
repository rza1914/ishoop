#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import asyncio
import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_SECRET_TOKEN = os.getenv('BOT_SECRET_TOKEN', 'default-bot-secret')
SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

class ProductParser:
    """پارسر هوشمند برای استخراج اطلاعات محصول از متن"""
    
    @staticmethod
    def extract_price(text: str) -> float:
        """استخراج قیمت از متن"""
        # الگوهای مختلف قیمت
        price_patterns = [
            r'(\d+(?:\.\d+)?)\s*درهم',
            r'(\d+(?:\.\d+)?)\s*AED',
            r'💳.*?(\d+(?:\.\d+)?)',
            r'قیمت.*?(\d+(?:\.\d+)?)',
            r'price.*?(\d+(?:\.\d+)?)',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        return 0.0
    
    @staticmethod
    def extract_category(text: str) -> str:
        """استخراج دسته‌بندی از هشتگ‌ها"""
        # نقشه دسته‌بندی‌ها
        category_map = {
            'بدلیجات': 'لوازم جانبی',
            'زیورات': 'لوازم جانبی', 
            'کیف': 'کیف و کفش',
            'کفش': 'کیف و کفش',
            'لباس': 'پوشاک',
            'پوشاک': 'پوشاک',
            'عطر': 'عطر و ادکلن',
            'ادکلن': 'عطر و ادکلن',
            'آرایش': 'آرایشی و بهداشتی',
            'بهداشتی': 'آرایشی و بهداشتی',
            'الکترونیک': 'الکترونیک',
            'موبایل': 'الکترونیک',
            'هندزفری': 'الکترونیک'
        }
        
        # جستجو در هشتگ‌ها
        hashtags = re.findall(r'#(\w+)', text)
        for hashtag in hashtags:
            for key, value in category_map.items():
                if key in hashtag:
                    return value
        
        # جستجو در متن
        text_lower = text.lower()
        for key, value in category_map.items():
            if key in text_lower:
                return value
                
        return 'سایر'
    
    @staticmethod
    def extract_product_name(text: str) -> str:
        """استخراج نام محصول"""
        lines = text.strip().split('\n')
        
        # اولین خط که حاوی حروف فارسی یا انگلیسی باشد
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('💳'):
                # حذف emoji ها از ابتدای خط
                clean_line = re.sub(r'^[^\w\u0600-\u06FF\s]+', '', line).strip()
                if clean_line:
                    return clean_line
        
        return 'محصول وارداتی'

class TelegramBot:
    """بات تلگرام آیشاپ برای ایمپورت محصولات"""
    
    def __init__(self):
        self.parser = ProductParser()
        self.session = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور شروع"""
        welcome_message = """
🤖 سلام! من بات آیشاپ هستم

قابلیت‌های من:
✅ تشخیص خودکار محصولات از پیام‌های forward شده
✅ تبدیل قیمت از درهم به تومان
✅ شناسایی دسته‌بندی از هشتگ‌ها
✅ اضافه کردن مستقیم به فروشگاه

برای شروع، پیام محصول را forward کنید!
        """
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """دستور راهنما"""
        help_text = """
📖 راهنمای استفاده:

1️⃣ پیام محصول را از کانال فروشگاه forward کنید
2️⃣ بات اطلاعات را تشخیص می‌دهد
3️⃣ قیمت را از درهم به تومان تبدیل می‌کند
4️⃣ دسته‌بندی را از هشتگ‌ها تشخیص می‌دهد
5️⃣ محصول را مستقیم به فروشگاه اضافه می‌کند

نمونه پیام صحیح:
گردنبند قلب زیبا
توضیحات محصول...
💳 قیمت: 25درهم
#بدلیجات #زیورات
        """
        await update.message.reply_text(help_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """پردازش پیام‌های forward شده"""
        message = update.message
        
        # بررسی اینکه پیام forward شده باشد
        if not message.forward_from and not message.forward_from_chat:
            await message.reply_text("❌ لطفاً پیام محصول را forward کنید")
            return
        
        text = message.text or message.caption or ""
        
        if not text:
            await message.reply_text("❌ متن پیام خالی است")
            return
        
        # نمایش پیام در حال پردازش
        processing_msg = await message.reply_text("🔄 در حال پردازش محصول...")
        
        try:
            # استخراج اطلاعات محصول
            product_name = self.parser.extract_product_name(text)
            price = self.parser.extract_price(text)
            category = self.parser.extract_category(text)
            
            # ایجاد داده‌های محصول
            product_data = {
                'name': product_name,
                'description': text.replace('\n', ' ').strip()[:500],  # محدود کردن طول
                'price': price,
                'category': category,
                'imageUrl': None,  # TODO: پردازش تصاویر
                'tags': re.findall(r'#(\w+)', text)
            }
            
            # ارسال به سرور
            success = await self.send_to_server(product_data)
            
            if success:
                response_text = f"""
✅ محصول با موفقیت اضافه شد!

📝 نام: {product_name}
💰 قیمت: {price:,.0f} درهم ({price*10000:,.0f} تومان)
📂 دسته‌بندی: {category}
🏷️ برچسب‌ها: {', '.join(product_data['tags']) if product_data['tags'] else 'ندارد'}
                """
                await processing_msg.edit_text(response_text)
            else:
                await processing_msg.edit_text("❌ خطا در اضافه کردن محصول به فروشگاه")
                
        except Exception as e:
            print(f"Error processing message: {e}")
            await processing_msg.edit_text(f"❌ خطا در پردازش: {str(e)}")
    
    async def send_to_server(self, product_data: dict) -> bool:
        """ارسال داده‌های محصول به سرور"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            headers = {
                'Content-Type': 'application/json',
                'X-Bot-Token': BOT_SECRET_TOKEN
            }
            
            async with self.session.post(
                f"{SERVER_URL}/api/bot/import-product",
                json=product_data,
                headers=headers
            ) as response:
                result = await response.json()
                return result.get('success', False)
                
        except Exception as e:
            print(f"Error sending to server: {e}")
            return False
    
    async def close_session(self):
        """بستن session"""
        if self.session:
            await self.session.close()

async def main():
    """تابع اصلی برای راه‌اندازی بات"""
    print("🤖 Starting iShop Telegram Bot...")
    
    # ایجاد application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    bot_instance = TelegramBot()
    
    # افزودن handlers
    application.add_handler(CommandHandler("start", bot_instance.start_command))
    application.add_handler(CommandHandler("help", bot_instance.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_instance.handle_message))
    
    try:
        # شروع بات
        print("✅ Bot is running...")
        await application.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        print("🛑 Bot stopped by user")
    finally:
        await bot_instance.close_session()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped")