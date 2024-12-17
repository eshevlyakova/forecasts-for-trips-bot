from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        'Доступные команды:\n'
        '/start — приветствует пользователя.\n'
        '/help — показывает помощь.\n'
        '/weather — запрос прогноза погоды для маршрута.'
    )

def register_handlers(dispatcher):
    dispatcher.include_router(router)
