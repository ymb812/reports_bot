from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Column, Url, SwitchTo, Start, Select
from aiogram_dialog.widgets.media import DynamicMedia
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import _
from core.dialogs.custom_content import CustomPager
from core.dialogs.callbacks import AdminCallbackHandler
from core.dialogs.getters import get_reports, get_sub_reports
from settings import settings


main_menu_dialog = Dialog(
    # menu
    Window(
        Const(text=_('PICK_REPORT')),
        CustomPager(
            Select(
                id='_reports_select',
                items='reports',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.name}'),
                on_click=AdminCallbackHandler.selected_report,
            ),
            id='reports_group',
            height=settings.items_per_page_height,
            width=settings.items_per_page_width,
            hide_on_single_page=True,
        ),
        getter=get_reports,
        state=MainMenuStateGroup.menu,
    ),

    # report_category
    Window(
        Const(text=_('PICK_REPORT')),
        CustomPager(
            Select(
                id='_sub_reports_select',
                items='sub_reports',
                item_id_getter=lambda item: item.id,
                text=Format(text='{item.file_name}'),
                on_click=AdminCallbackHandler.selected_sub_report,
            ),
            id='sub_reports_group',
            height=settings.items_per_page_height,
            width=settings.items_per_page_width,
            hide_on_single_page=True,
        ),
        SwitchTo(Const(text=_('BACK_BUTTON')), id='go_to_reports', state=MainMenuStateGroup.menu),
        getter=get_sub_reports,
        state=MainMenuStateGroup.report_category,
    ),
)
