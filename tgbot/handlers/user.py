from aiogram import types
from aiogram.filters.command import CommandObject
from redis.asyncio import Redis

from database.redis.main import get_char_codes, get_converted_amount, get_currency_info
from keyboards.inline import basic
from data import config


async def start_handler(message: types.Message) -> None:
    m = [
        "/start - главное меню\n"
        "/exchange USD RUB 10 - отображает стоимость 10 долларов в рублях\n"
        "/rates - актуальные курсы валют"
    ]
    await message.answer(''.join(m))


async def exchange_handler(
    message: types.Message, 
    command: CommandObject, 
    cache_pool: Redis
) -> None:
    if command.args:
        if len(command.args.split(' ')) == 3:
            char_code_in, char_code_out, amount = command.args.split(' ')
            if char_code_in in await get_char_codes(cache_pool):
                if char_code_out in await get_char_codes(cache_pool):
                    await message.answer(f"Конвертация {char_code_in} в {char_code_out}")
                    result = await get_converted_amount(cache_pool, char_code_in, char_code_out, amount)
                    await message.answer(f"{amount} {char_code_in} = {result} {char_code_out}")
                else:
                    await message.answer(f"{char_code_out} не существует!")
            else:
                await message.answer(f"{char_code_in} не существует!")
        else:
            m = [
                "Неверное количество аргументов!\n"
                "Пример:\n"
                "<code>/exchange USD RUB 10</code>"
            ]
            await message.answer(''.join(m))
    else:
        m = [
            "Неверный формат ввода!\n"
            "Пример:\n"
            "<code>/exchange USD RUB 10</code>"
        ]
        await message.answer(''.join(m))


async def get_msg(
    cache_pool: Redis, 
    cc_in_msg: list
) -> str:
    m = ''
    cur_info = await get_currency_info(cache_pool, cc_in_msg)
    for i in range(len(cc_in_msg)):
        m += f"<b>{cc_in_msg[i]}</b>\n"
        m += f"Единиц: <code>{cur_info[i].get('Nominal')}</code>\n"
        m += f"Валюта: <code>{cur_info[i].get('Name')}</code>\n"
        m += f"Курс: <code>{cur_info[i].get('Value')}</code>\n\n"
    return m


async def rates_handler(
    message: types.Message, 
    cache_pool: Redis
) -> None:
    page = 0
    char_codes = await get_char_codes(cache_pool)
    char_codes.remove('RUB')
    cc_in_msg = char_codes[page*config.NUM_CUR_IN_MSG:(page+1)*config.NUM_CUR_IN_MSG]
    m = await get_msg(cache_pool, cc_in_msg)

    await message.answer(
        text=m, 
        reply_markup=basic.currencies_paginator(0, len(char_codes))
    )


async def currencies_handler(
    call: types.CallbackQuery, 
    callback_data: basic.Pagination,
    cache_pool: Redis
) -> None:
    page_num = int(callback_data.page)
    page = page_num - 1 

    if callback_data.action == "next":
        page = page_num + 1 

    currencies = await get_char_codes(cache_pool)
    currencies.remove('RUB')
    cc_in_msg = currencies[page*config.NUM_CUR_IN_MSG:(page+1)*config.NUM_CUR_IN_MSG]
    m = await get_msg(cache_pool, cc_in_msg)

    await call.message.edit_text(
        text=m,
        reply_markup=basic.currencies_paginator(page, len(currencies))
    )
    await call.answer()