from redis.asyncio import Redis


async def wait_redis(url: str) -> Redis:
    redis = Redis.from_url(url=url, decode_responses=True)
    return redis

