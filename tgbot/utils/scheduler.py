import asyncio
import aioschedule
from redis.asyncio import Redis

from database.redis.main import update_currency


async def scheduler1(cache_pool: Redis):
    aioschedule.every().day.do(update_currency, cache_pool)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        