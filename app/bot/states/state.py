from aiogram.fsm.state import StatesGroup, State


# Stage для создания сделки в Bitrix
class MainState(StatesGroup):
    check_imei = State()

