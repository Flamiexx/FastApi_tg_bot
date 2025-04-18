from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging
import os
from dotenv import load_dotenv
from app.bot.handlers import router

load_dotenv(dotenv_path="token.env")
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

