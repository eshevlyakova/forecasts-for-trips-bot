from aiogram.fsm.state import StatesGroup, State

class WeatherForm(StatesGroup):
    waiting_for_start = State()
    waiting_for_end = State()
    waiting_for_intermediate = State()
    waiting_for_interval = State()
