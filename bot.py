import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types.bot_command import BotCommand
from dotenv import load_dotenv
from app.handlers import router
from app.commands import FILMS_COMMAND

load_dotenv()

TOKEN = getenv("TOKEN_BOT")


dp = Dispatcher()
dp.include_router(router)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Зaпуск ботa"),
            BotCommand(
                command=FILMS_COMMAND, description="Перегляд списку фільмів"
            ),
        ]
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
