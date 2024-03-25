from aiogram.fsm.state import State, StatesGroup


class RegistrationStateGroup(StatesGroup):
    input_phone = State()
