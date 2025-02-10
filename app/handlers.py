from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from .commands import FILMS_COMMAND
from .database import get_data
from .keyboards import menu_keyboard, film_keyboard, FilmsCallback
from aiogram import F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import URLInputFile
from .schemas import Film


router = Router()
DATABASE = "data.json"


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, {message.from_user.full_name}!", reply_markup=menu_keyboard()
    )


# @router.message()
# async def echo_handler(message: Message):
#     await message.reply(message.text.upper())


@router.message(Command(FILMS_COMMAND))
@router.message(F.text == "Фільми")
async def films(message: Message) -> None:
    data = get_data(DATABASE)
    markup_films = film_keyboard(data)

    await message.answer(f"Оберіть фільм:", reply_markup=markup_films)


@router.callback_query(FilmsCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmsCallback) -> None:
    data_film: dict = get_data(DATABASE, film_id=callback_data.id)

    
    film = Film(**data_film)

    text_message = (
        f"Title: {film.title}\n\nDescription: {film.desc}\n\nRating: {film.rating}"
    )

    await callback.message.answer_photo(
        caption=text_message,
        photo=URLInputFile(
            url=data_film["photo"],
            filename=f"{film.title}_poster.{film.photo.split('.')[-1]}",
        ),
    )

    await callback.answer()
