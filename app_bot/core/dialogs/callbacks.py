from tortoise.exceptions import IntegrityError
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select, SwitchPage
from core.states.main_menu import MainMenuStateGroup
from core.states.admin_menu import AdminStateGroup, AddUserStateGroup
from core.database.models import Report, SubReport, ReportAccess, User
from core.utils.texts import _
from settings import settings


class AdminCallbackHandler:
    @classmethod
    async def selected_report(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):

        dialog_manager.dialog_data['report_id'] = item_id

        # send content
        report = await Report.get_or_none(id=item_id)
        if report:
            await dialog_manager.switch_to(MainMenuStateGroup.report_category)
        else:
            await callback.message.answer(text='Отчет не найден')


    @classmethod
    async def selected_sub_report(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):

        dialog_manager.dialog_data['sub_report_id'] = item_id

        # send content
        sub_report = await SubReport.get_or_none(id=item_id)
        if sub_report:
            await callback.message.answer_document(
                document=FSInputFile(path=f'{settings.base_files_dir}/{sub_report.file_name}')
            )
        else:
            await callback.message.answer(text='Отчет не найден')


    @classmethod
    async def selected_user(
            cls,
            callback: CallbackQuery,
            widget: Select,
            dialog_manager: DialogManager,
            item_id: str,
    ):

        dialog_manager.dialog_data['user_id'] = item_id
        await dialog_manager.switch_to(AdminStateGroup.user_menu)


    @staticmethod
    async def send_reports(
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager
    ):
        reports = await Report.all()
        reports_msg = ''
        for report in reports:
            reports_msg += f'{report.id}. {report.name}\n'

        await callback.message.answer(text=reports_msg)


    @staticmethod
    async def give_or_revoke_access(
            callback: CallbackQuery,
            widget: Button,
            dialog_manager: DialogManager
    ):
        if 'give_access' in callback.data:
            dialog_manager.dialog_data['revoke_access'] = False
        elif 'revoke_access' in callback.data:
            dialog_manager.dialog_data['revoke_access'] = True

        await dialog_manager.switch_to(AdminStateGroup.edit_access)


    @staticmethod
    async def entered_reports(
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value: str,
    ):
        user_id = dialog_manager.dialog_data['user_id']
        error_flag = False

        reports = message.text.strip().split(',')
        if dialog_manager.dialog_data['revoke_access']:
            action = 'удален'
            for report in reports:
                if report.isdigit():
                    await ReportAccess.filter(user_id=user_id, report_id=report).delete()

        else:
            action = 'выдан'
            for report in reports:
                try:
                    if report.isdigit():
                        await ReportAccess.get_or_create(user_id=user_id, report_id=report)
                except Exception as e:
                    await message.answer(text=_('ACCESS_ERROR', report_id=report))
                    error_flag = True

        if not error_flag:
            await message.answer(text=_('ACCESS_IS_EDITED', action=action))

        await dialog_manager.switch_to(AdminStateGroup.user_menu)


class AddUserCallbackHandler:
    @classmethod
    async def entered_data(
            cls,
            message: Message,
            widget: ManagedTextInput,
            dialog_manager: DialogManager,
            value: str,
    ):
        if widget.widget.widget_id == 'input_fio':
            dialog_manager.dialog_data['fio'] = value
            await dialog_manager.switch_to(AddUserStateGroup.input_phone)

        elif widget.widget.widget_id == 'input_phone':
            dialog_manager.dialog_data['phone'] = value
            await dialog_manager.switch_to(AddUserStateGroup.input_reports_access)

        elif widget.widget.widget_id == 'input_reports':
            # create user
            try:
                user = await User.create(
                    fio=dialog_manager.dialog_data['fio'],
                    phone=dialog_manager.dialog_data['phone'],
                )
            except IntegrityError:
                await message.answer(text=_('INPUT_PHONE_ADMIN_WRONG'))
                return

            # give access
            error_flag = False
            reports = message.text.strip().split(',')
            for report in reports:
                try:
                    if report.isdigit():
                        await ReportAccess.get_or_create(user_id=user.id, report_id=report)
                except Exception as e:
                    await message.answer(text=_('ACCESS_ERROR', report_id=report))
                    error_flag = True

            if not error_flag:
                await message.answer(text=_('ACCESS_IS_EDITED', action='выдан'))

            await dialog_manager.start(AdminStateGroup.users_list)
