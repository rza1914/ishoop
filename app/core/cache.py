from fastapi_cache import FastAPICache, Coder
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.core.config import settings

async def get_redis():
    return aioredis.from_url(settings.REDIS_URL, encoding="utf8", decode_responses=True)

async def init_cache():
    redis = await get_redis()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
