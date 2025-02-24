from random import randint

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
