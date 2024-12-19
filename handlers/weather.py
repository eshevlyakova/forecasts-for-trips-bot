from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from services.weather_service import get_weather_report
from models.states import WeatherForm
from handlers.utils import get_yes_no_keyboard, get_interval_inline_keyboard

router = Router()

def contains_digit(s: str) -> bool:
    return any(char.isdigit() for char in s)

@router.message(Command("weather"))
async def weather_command(message: Message, state: FSMContext):
    await state.set_state(WeatherForm.waiting_for_start)
    await message.answer('Введите начальную точку маршрута:')

@router.message(WeatherForm.waiting_for_start)
async def process_start(message: Message, state: FSMContext):
    start_point = message.text
    if contains_digit(start_point):
        await message.answer('Название города не должно содержать цифр. Пожалуйста, введите корректное название начальной точки маршрута:')
        return
    await state.update_data(start=start_point)
    await state.set_state(WeatherForm.waiting_for_end)
    await message.answer('Введите конечную точку маршрута:')

@router.message(WeatherForm.waiting_for_end)
async def process_end(message: Message, state: FSMContext):
    end_point = message.text
    if contains_digit(end_point):
        await message.answer('Название города не должно содержать цифр. Пожалуйста, введите корректное название конечной точки маршрута:')
        return
    await state.update_data(end=end_point)
    await state.set_state(WeatherForm.waiting_for_intermediate)
    await message.answer(
        'Есть ли промежуточные остановки на маршруте?',
        reply_markup=get_yes_no_keyboard(),
    )

@router.message(WeatherForm.waiting_for_intermediate, F.text.in_({"Да", "Нет"}))
async def process_intermediate(message: Message, state: FSMContext):
    if message.text == "Да":
        await state.update_data(intermediate=[])
        await message.answer('Введите промежуточную точку маршрута (или напишите "Готово", если больше нет):')
    else:
        await state.update_data(intermediate=None)
        await ask_time_interval(message, state)

@router.message(WeatherForm.waiting_for_intermediate)
async def process_add_intermediate(message: Message, state: FSMContext):
    intermediate_point = message.text
    if intermediate_point.lower() == "готово":
        await ask_time_interval(message, state)
    else:
        if contains_digit(intermediate_point):
            await message.answer('Название города не должно содержать цифр. Пожалуйста, введите корректное название промежуточной точки маршрута или напишите "Готово":')
            return
        data = await state.get_data()
        intermediate_points = data.get('intermediate', [])
        intermediate_points.append(intermediate_point)
        await state.update_data(intermediate=intermediate_points)
        await message.answer('Введите следующую промежуточную точку или напишите "Готово":')

async def ask_time_interval(message: Message, state: FSMContext):
    await state.set_state(WeatherForm.waiting_for_interval)
    await message.answer(
        'Выберите временной интервал прогноза:',
        reply_markup=get_interval_inline_keyboard(),
    )

@router.callback_query(F.data.startswith("interval_"))
async def process_interval_callback(callback: CallbackQuery, state: FSMContext):
    interval = int(callback.data.split('_')[1])
    await state.update_data(interval=interval)

    data = await state.get_data()
    start = data.get('start')
    end = data.get('end')
    intermediate = data.get('intermediate')
    interval_days = data.get('interval')

    weather_report = await get_weather_report(start, end, intermediate, interval_days)
    await state.clear()
    await callback.message.answer(weather_report)
    await callback.answer()

def register_handlers(dispatcher):
    dispatcher.include_router(router)
