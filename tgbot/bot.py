import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from redis.asyncio import Redis
from data import config
from utils import wait_redis, scheduler1

from database.redis.main import update_currency
import handlers


async def create_db_connections(dp: Dispatcher) -> None:
    try:
        cache_pool = await wait_redis(url=config.REDIS_URL)
    except Exception as e:
        print(f"Failed to connect to Redis ({e})")
        exit(1)
    else:
        print("Succesfully connected to Redis")
    dp["cache_pool"] = cache_pool


async def close_db_connections(dp: Dispatcher) -> None:
    if "cache_pool" in dp.workflow_data:
        cache_pool: Redis = dp["cache_pool"]
        await cache_pool.aclose()


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(handlers.prepare_user_router())


async def setup_aiogram(dp: Dispatcher, bot: Bot) -> None:
    await create_db_connections(dp)
    setup_handlers(dp)
    await update_currency(dp["cache_pool"])
    asyncio.create_task(scheduler1(dp["cache_pool"]))


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(dispatcher, bot)


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher) -> None:
    await close_db_connections(dispatcher)
    await dispatcher.storage.close()


def main() -> None:
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(
        storage=MemoryStorage()
        # storage=RedisStorage(
        #     redis=Redis.from_url(config.REDIS_URL),
        #     key_builder=DefaultKeyBuilder(with_bot_id=True)
        # )
    )

    dp.startup.register(aiogram_on_startup_polling)
    dp.shutdown.register(aiogram_on_shutdown_polling)
    asyncio.run(dp.start_polling(bot))

if __name__ == "__main__":
    main()
    