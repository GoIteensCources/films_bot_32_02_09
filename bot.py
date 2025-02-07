import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    print(message)
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message()
async def echo_handler(message: Message):
    await message.reply(message.text.upper())

    
    
async def main() -> None:
    bot = Bot(token=TOKEN, 
              default=DefaultBotProperties(parse_mode=ParseMode.HTML)
              )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
