from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    ReplyKeyboardBuilder,
)

BUTTON_LIST_FILMS = "Перелік фільмів"
BUTTON_ADD_FILM = "Додати фільм"
BUTTON_DELETE_FILM = "Видалити фільм"

PAGE_SIZE = 3


def menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text=BUTTON_LIST_FILMS)
    builder.button(text=BUTTON_ADD_FILM)
    builder.button(text=BUTTON_DELETE_FILM)

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup


class FilmsCallback(CallbackData, prefix="films", sep=";"):
    id: int
    title: str


# def film_keyboard(list_films: list):
#     builder = InlineKeyboardBuilder()

#     for id, data_film in enumerate(list_films):
#         callback = FilmsCallback(id=id, title=data_film["title"])

#         builder.button(text=callback.title, callback_data=callback.pack())

#         builder.adjust(1, repeat=True)
#     return builder.as_markup()


def film_keyboard(films_list: list[dict], page: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    total_pages = (len(films_list) + PAGE_SIZE - 1) // PAGE_SIZE
    start_idx = (page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE

    for index, film_data in enumerate(films_list[start_idx:end_idx], start=start_idx):
        callback_film = FilmsCallback(id=index, **film_data)
        builder.button(
            text=f"{callback_film.title}", callback_data=callback_film.pack()
        )
        builder.adjust(1, repeat=True)

    nav_buttons = []

    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton(text="< Назад", callback_data=f"page_{page - 1}")
        )
    if page < total_pages:
        nav_buttons.append(
            InlineKeyboardButton(text="Вперед >", callback_data=f"page_{page + 1}")
        )

    if nav_buttons:
        builder.row(*nav_buttons)

    return builder.as_markup()
