from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis
from app.core.config import settings

async def init_limiter():
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPILimiter.init(redis)
