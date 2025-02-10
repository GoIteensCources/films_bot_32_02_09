from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


BUTTON_LIST_FILMS = "Перелік фільмів"


class FilmsCallback(CallbackData, prefix="films", sep=";"):
    id: int
    title: str


def menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text=BUTTON_LIST_FILMS)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup


def film_keyboard(list_films: list):
    builder = InlineKeyboardBuilder()

    for id, data_film in enumerate(list_films):
        callback = FilmsCallback(id=id, title=data_film["title"])

        builder.button(text=callback.title, callback_data=callback.pack())

        builder.adjust(1, repeat=True)
    return builder.as_markup()
