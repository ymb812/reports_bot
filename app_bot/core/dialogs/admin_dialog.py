from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Start, Select, Button
from core.states.admin_menu import AdminStateGroup, AddUserStateGroup
from core.utils.texts import _
from core.dialogs.custom_content import CustomPager
from core.dialogs.callbacks import AdminCallbackHandler
from core.dialogs.getters import get_users
from settings import settings


admin_menu_dialog = Dialog(
    # menu
    Window(
        Const(text=_('PICK_ACTION')),
        Column(
            Start(Const(text=_('ADD_USER_BUTTON')), id='go_to_add_user', state=AddUserStateGroup.input_fio),
            SwitchTo(Const(text=_('USERS_BUTTON')), id='go_to_users_list', state=AdminStateGroup.users_list),
            Button(Const(text=_('REPORTS_LIST_BUTTON')), id='reports_list', on_click=AdminCallbackHandler.send_reports),
        ),
        state=AdminStateGroup.menu,
    ),

    # users list
    Window(
        Const(text=_('PICK_ACTION')),
        CustomPager(
            Select(
                id='_users_select',
                items='users',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.fio}'),
                on_click=AdminCallbackHandler.selected_user,
            ),
            id='users_group',
            height=settings.items_per_page_height,
            width=settings.items_per_page_width,
            hide_on_single_page=True,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_menu', state=AdminStateGroup.menu),
        getter=get_users,
        state=AdminStateGroup.users_list,
    ),

    # user menu
    Window(
        Const(text=_('PICK_ACTION')),
        Column(
            Button(Const(text=_('GIVE_ACCESS_BUTTON')), id='give_access',
                   on_click=AdminCallbackHandler.give_or_revoke_access),
            Button(Const(text=_('REVOKE_ACCESS_BUTTON')), id='revoke_access',
                   on_click=AdminCallbackHandler.give_or_revoke_access),
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_users_list', state=AdminStateGroup.users_list),
        state=AdminStateGroup.user_menu,
    ),

    # exhibit input
    Window(
        Format(text=_('INPUT_REPORTS_TO_EDIT_ACCESS')),
        TextInput(
            id='input_reports',
            type_factory=str,
            on_success=AdminCallbackHandler.entered_reports
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_user_menu', state=AdminStateGroup.user_menu),
        state=AdminStateGroup.edit_access
    ),
)
