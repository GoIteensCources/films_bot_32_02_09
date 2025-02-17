from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from .commands import FILMS_COMMAND, ADD_FILM_COMMAND
from .database import get_data ,add_film_to_db
from .keyboards import menu_keyboard, film_keyboard, FilmsCallback, BUTTON_LIST_FILMS, BUTTON_ADD_FILM
from aiogram import F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import URLInputFile
from .schemas import Film
from .fsm import FilmForm
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove


router = Router()
DATABASE = "data.json"

# command  /start
@router.message(CommandStart()) # or /start
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Hello, {message.from_user.full_name}!", 
        reply_markup=menu_keyboard()
    )


# list of films
@router.message(Command(FILMS_COMMAND))
@router.message(F.text == BUTTON_LIST_FILMS)
async def films(message: Message) -> None:
    data = get_data(DATABASE)
    markup_films = film_keyboard(data)

    await message.answer(f"Оберіть фільм:", reply_markup=markup_films)



@router.callback_query(F.data.startswith("page_"))
async def pages_films(callback: CallbackQuery) -> None:
    page =  int(callback.data.split("_")[1])    
    data = get_data(DATABASE)
    markup_films = film_keyboard(data, page)
    await callback.message.edit_reply_markup(reply_markup=markup_films)
    await callback.answer()



# info about filb 
@router.callback_query(FilmsCallback.filter())
async def callb_film(callback: CallbackQuery, callback_data: FilmsCallback) -> None:
    data_film: dict = get_data(DATABASE, film_id=callback_data.id)
    
    film = Film(**data_film)
    text_message = (
        f"Title: {film.title}\n\nDescription: {film.desc}\n\nRating: {film.rating}"
    )
    if film.photo.startswith("http"):
        photo_data = URLInputFile(
                url=data_film["photo"],
                filename=f"{film.title}_poster.{film.photo.split('.')[-1]}")
    else:
        photo_data = film.photo
    
    await callback.message.answer_photo(
        caption=text_message,
        photo=photo_data,
    )
    
    await callback.answer()

    
    
    
    
@router.message(Command(ADD_FILM_COMMAND))
@router.message(F.text == BUTTON_ADD_FILM)
async def add_film(message: Message, state: FSMContext) -> None:    
    await message.answer(f"Починаємо додавати фільм")
    await state.set_state(FilmForm.title)
    await message.answer("Ведіть назву фільму", 
                         reply_markup=ReplyKeyboardRemove())
    

@router.message(FilmForm.title)
async def add_film_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(FilmForm.desc)
    await message.answer("Ведіть опис фільму")
    
    
@router.message(FilmForm.desc)
async def add_film_desc(message: Message, state: FSMContext) -> None:
    await state.update_data(desc=message.text)
    await state.set_state(FilmForm.rating)
    await message.answer("Ведіть рейтинг фільму")
    
    
@router.message(FilmForm.rating)
async def add_film_rating(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():    
        await state.update_data(rating=message.text)
        await state.set_state(FilmForm.url)
        await message.answer("Ведіть посилання на фільм")
    else:
        await message.answer("Ведіть рейтинг фільму")
    
    
@router.message(FilmForm.url)
async def add_film_url(message: Message, state: FSMContext) -> None:
    await state.update_data(url=message.text)
    await state.set_state(FilmForm.photo)
    await message.answer("Ведіть посилання на постер фільму")

    
@router.message(FilmForm.photo)
async def add_film_photo(message: Message, state: FSMContext) -> None:
    
    if message.photo:
        photo_id = message.photo[-1].file_id        
        data = await state.update_data(photo=photo_id)
        
        film = Film(**data)      
          
        add_film_to_db(film.model_dump(), DATABASE)
        
        await state.clear()        
        await message.answer(f"Дякую за введену інформацію! Фільм збережено!",
                        reply_markup=menu_keyboard())
    
    else:
        data = await state.get_data()
        await message.answer(f"Це не фото, додай афішу до : {data.get('title')}")
