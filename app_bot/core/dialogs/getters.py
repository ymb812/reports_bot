from tortoise.expressions import Q
from aiogram.enums import ContentType
from core.database.models import User, SubReport, ReportAccess, Post
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from settings import settings


async def get_welcome_msg(dialog_manager: DialogManager, **kwargs):
    welcome_post = await Post.get(id=settings.welcome_post_id)

    return {
        'caption': welcome_post.text,
        'photo': MediaAttachment(ContentType.PHOTO, url=welcome_post.photo_file_id)
    }


async def get_reports(dialog_manager: DialogManager, **kwargs):
    reports = await ReportAccess.filter(user__user_id=dialog_manager.event.from_user.id).all()
    reports_data = [await report.report for report in reports]

    return {
        'reports': reports_data
    }


async def get_sub_reports(dialog_manager: DialogManager, **kwargs):
    sub_reports = await SubReport(parent_report_id=dialog_manager.dialog_data['report_id']).all()
    sub_reports_data = [sub_report for sub_report in sub_reports]

    return {
        'sub_reports': sub_reports_data
    }


async def get_users(dialog_manager: DialogManager, **kwargs):
    users = await User.filter(~Q(phone=None)).all()

    return {
        'users': users
    }
