from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data import config


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int


def get_num_pages(len: int):
    num = len // config.NUM_CUR_IN_MSG
    if (len % config.NUM_CUR_IN_MSG) != 0:
        num += 1
    return num


def currencies_paginator(
    page: int, 
    num_cur: int, 
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if num_cur > config.NUM_CUR_IN_MSG:
        if page == 0:
            builder.row(
                InlineKeyboardButton(
                    text=">", 
                    callback_data=Pagination( 
                        action="next", 
                        page=page
                    ).pack()
                )
            )
        elif page == get_num_pages(num_cur) - 1:
            builder.row(
                InlineKeyboardButton(
                    text="<", 
                    callback_data=Pagination( 
                        action="prev", 
                        page=page
                    ).pack()
                )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text="<", 
                    callback_data=Pagination( 
                        action="prev", 
                        page=page
                    ).pack()
                ),
                InlineKeyboardButton(
                    text=">", 
                    callback_data=Pagination( 
                        action="next", 
                        page=page
                    ).pack()
                ),
                width=2
            )
    
    return builder.as_markup()



