#!/usr/bin/env python3
"""
Telegram Bot Starter Script
"""
import sys
import os
import asyncio

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot.bot import main

if __name__ == "__main__":
    print("Starting Telegram Product Importer Bot...")
    print("Make sure the FastAPI backend is running on http://localhost:8000")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped gracefully!")
    except Exception as e:
        print(f"Error: {e}")