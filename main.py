import aiogram 
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router
from config import BOT_TOKEN
from src.handlers import router 
from aiogram.fsm.storage.memory import MemoryStorage


bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    logging.basicConfig(level=logging.INFO)