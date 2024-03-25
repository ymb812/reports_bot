from aiogram.fsm.state import State, StatesGroup


class AdminStateGroup(StatesGroup):
    menu = State()
    users_list = State()

    user_menu = State()
    edit_access = State()


class AddUserStateGroup(StatesGroup):
    input_fio = State()
    input_phone = State()
    input_reports_access = State()
