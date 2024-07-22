from aiogram import Router, F 
from aiogram.filters import Command, CommandStart

from handlers import user
from keyboards.inline.basic import Pagination


def prepare_user_router() -> Router:
    user_router = Router()

    user_router.message.register(user.start_handler, CommandStart())
    user_router.message.register(user.exchange_handler, Command('exchange'))
    user_router.message.register(user.rates_handler, Command('rates'))
    
    user_router.callback_query.register(
        user.currencies_handler, 
        Pagination.filter(F.action.in_(["prev", "next"]))
    )

    return user_router