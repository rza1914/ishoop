# app/api/v1/endpoints/currency.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os
from typing import Dict

router = APIRouter()

# مسیر فایل تنظیمات
SETTINGS_FILE = "settings.json"

class CurrencyRateRequest(BaseModel):
    rate: float

class CurrencyRateResponse(BaseModel):
    rate: float
    currency: str = "AED_TO_TOMAN"

def get_current_rate() -> float:
    """دریافت نرخ فعلی از فایل یا مقدار پیش‌فرض"""
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return float(settings.get('aed_to_toman_rate', 11000.0))
    except Exception as e:
        print(f"Error reading rate: {e}")
    return 11000.0

def save_rate(rate: float) -> bool:
    """ذخیره نرخ در فایل"""
    try:
        # خواندن تنظیمات فعلی
        settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        
        # آپدیت نرخ
        settings['aed_to_toman_rate'] = rate
        
        # ذخیره
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving rate: {e}")
        return False

@router.get("/rate", response_model=CurrencyRateResponse)
async def get_currency_rate():
    """دریافت نرخ فعلی درهم به تومان"""
    rate = get_current_rate()
    return CurrencyRateResponse(rate=rate)

@router.post("/rate", response_model=CurrencyRateResponse)
async def update_currency_rate(rate_request: CurrencyRateRequest):
    """آپدیت نرخ درهم به تومان"""
    success = save_rate(rate_request.rate)
    if not success:
        raise HTTPException(status_code=500, detail="Error saving rate")
    
    return CurrencyRateResponse(rate=rate_request.rate)