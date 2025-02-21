from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from .commands import FILMS_COMMAND, ADD_FILM_COMMAND
from .database import get_data, add_film_to_db
from .keyboards import (
    menu_keyboard,
    film_keyboard,
    FilmsCallback,
    BUTTON_LIST_FILMS,
    BUTTON_ADD_FILM,
)
from aiogram import F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import URLInputFile

from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from random import randint

router_calb = Router()
DATABASE = "data.json"


def inline_learn_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="GiTHAUb", url="https://github.com/GoIteensCources/films_bot_32_02_09"
        )
    )

    builder.row(InlineKeyboardButton(text="random Value", callback_data="value_random"))
    builder.add(InlineKeyboardButton(text="10", callback_data="value_10"))

    return builder.as_markup()


@router_calb.message(Command("inline"))
async def inline_handler(message: Message) -> None:
    await message.answer(f"Инлайн кнопки:", reply_markup=inline_learn_keyboard())


@router_calb.callback_query(F.data.startswith("value_"))
async def callb_film(callback: CallbackQuery) -> None:
    if callback.data == "value_random":
        await callback.message.answer(str(randint(1, 100)))

    if callback.data == "value_10":
        await callback.message.answer("10")

    await callback.answer("Thanks", show_alert=True)
