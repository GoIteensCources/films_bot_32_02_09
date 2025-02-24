import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types.bot_command import BotCommand
from dotenv import load_dotenv

from app.calbeck_learn_handler import router_calb
from app.commands import ADD_FILM_COMMAND, DELETE_FILM_COMMAND, FILMS_COMMAND
from app.handlers import router

load_dotenv()

TOKEN = getenv("TOKEN_BOT")


dp = Dispatcher()
dp.include_router(router)
dp.include_router(router_calb)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Зaпуск ботa"),
            BotCommand(command=FILMS_COMMAND, description="Перегляд списку фільмів"),
            BotCommand(command=ADD_FILM_COMMAND, description="Додати фільм"),
            BotCommand(command=DELETE_FILM_COMMAND, description="Видалити фільм"),
        ]
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        # stream=sys.stdout,
        filemode="w",
        filename="botlog.log",
    )
    asyncio.run(main())
