import logging
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from handlers import start, help, weather

load_dotenv()
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

if not API_TOKEN:
    raise ValueError("Токен бота не найден. Убедитесь, что он указан в файле .env")
if not WEATHER_API_KEY:
    raise ValueError("Ключ API для прогноза погоды не найден. Убедитесь, что он указан в файле .env")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)

start.register_handlers(dispatcher)
help.register_handlers(dispatcher)
weather.register_handlers(dispatcher)

async def main():
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.close()

if __name__ == '__main__':
    asyncio.run(main())
