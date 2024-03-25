from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Start, Select, Button
from core.states.admin_menu import AdminStateGroup, AddUserStateGroup
from core.utils.texts import _
from core.dialogs.custom_content import CustomPager
from core.dialogs.callbacks import AdminCallbackHandler, AddUserCallbackHandler
from core.dialogs.getters import get_users
from settings import settings


add_user_dialog = Dialog(
    # fio input
    Window(
        Format(text=_('INPUT_FIO')),
        TextInput(
            id='input_fio',
            type_factory=str,
            on_success=AddUserCallbackHandler.entered_data
        ),
        Start(Const(text=_('BACK_BUTTON')), id='go_to_admin_menu', state=AdminStateGroup.menu),
        state=AddUserStateGroup.input_fio
    ),

    # phone input
    Window(
        Format(text=_('INPUT_PHONE_ADMIN')),
        TextInput(
            id='input_phone',
            type_factory=str,
            on_success=AddUserCallbackHandler.entered_data
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_fio', state=AddUserStateGroup.input_fio),
        state=AddUserStateGroup.input_phone
    ),

    # fio input
    Window(
        Format(text=_('INPUT_REPORTS_TO_EDIT_ACCESS')),
        TextInput(
            id='input_reports',
            type_factory=str,
            on_success=AddUserCallbackHandler.entered_data
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_phone', state=AddUserStateGroup.input_phone),
        state=AddUserStateGroup.input_reports_access
    ),
)
