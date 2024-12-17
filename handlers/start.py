from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        'Привет! Я бот для получения прогноза погоды. Используй команду /help, чтобы узнать, как мной пользоваться.'
    )

def register_handlers(dispatcher):
    dispatcher.include_router(router)
