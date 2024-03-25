import logging
from aiogram import Bot, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram_dialog import DialogManager, StartMode
from core.states.registration import RegistrationStateGroup
from core.states.main_menu import MainMenuStateGroup
from core.utils.texts import set_user_commands, set_admin_commands, _
from core.database.models import User, Post
from settings import settings


logger = logging.getLogger(__name__)
router = Router(name='Start router')


@router.message(Command(commands=['start']))
async def check_access(message: types.Message, bot: Bot, state: FSMContext, dialog_manager: DialogManager,
                       command: CommandObject):
    await state.clear()

    # add admin
    if command.args == settings.admin_password.get_secret_value():
        await state.clear()
        await message.answer(text=_('NEW_ADMIN_TEXT'))

        await User.update_admin_data(user_id=message.from_user.id, username=message.from_user.username, status='admin')
        await set_admin_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))
        return


    # send main menu if user already exists
    user = await User.get_or_none(user_id=message.from_user.id)
    if user:
        await dialog_manager.start(state=MainMenuStateGroup.menu, mode=StartMode.RESET_STACK)
        return

    await message.answer(text=_('INPUT_PHONE'))
    await state.set_state(RegistrationStateGroup.input_phone)


@router.message(RegistrationStateGroup.input_phone)
async def start_handler(message: types.Message, bot: Bot, state: FSMContext, dialog_manager: DialogManager):
    phone = message.text.strip()

    user = await User.get_or_none(phone=phone)
    if not user:  # ignore start users with incorrect phone
        await message.answer(text=_('INPUT_PHONE_WRONG'))
        return

    # save tg data
    user.user_id = message.from_user.id
    user.username = message.from_user.username
    await user.save()

    user = await User.get(user_id=message.from_user.id)
    if user.status == 'admin':
        await set_admin_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))
    else:
        await set_user_commands(bot=bot, scope=types.BotCommandScopeChat(chat_id=message.from_user.id))

    # send main menu
    await state.clear()
    await dialog_manager.start(state=MainMenuStateGroup.menu, mode=StartMode.RESET_STACK)
