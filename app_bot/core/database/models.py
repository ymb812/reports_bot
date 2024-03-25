import logging
from tortoise import fields
from tortoise.models import Model


logger = logging.getLogger(__name__)


class User(Model):
    class Meta:
        table = 'users'
        ordering = ['created_at']

    id = fields.IntField(pk=True, index=True)
    user_id = fields.BigIntField(unique=True, index=True, null=True)
    username = fields.CharField(max_length=32, index=True, null=True)
    fio = fields.CharField(max_length=64, null=True)
    phone = fields.CharField(max_length=16, unique=True, null=True)
    status = fields.CharField(max_length=32, null=True)  # admin

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


    @classmethod
    async def update_admin_data(cls, user_id: int, username: str, status: str):
        user = await cls.get_or_none(user_id=user_id)
        if user is None:
            await cls.create(
                user_id=user_id,
                username=username,
                status=status
            )
        else:
            user.status = status
            await user.save()


class Report(Model):
    class Meta:
        table = 'reports'
        ordering = ['id']

    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=64)
    text = fields.TextField(null=True)
    file_id = fields.CharField(max_length=256, null=True)


class ReportAccess(Model):
    class Meta:
        table = 'reports_access'
        ordering = ['id']
        unique_together = ('user', 'report')

    id = fields.IntField(pk=True, index=True)
    user = fields.ForeignKeyField(model_name='models.User', to_field='id')
    report = fields.ForeignKeyField(model_name='models.Report', to_field='id')


class Dispatcher(Model):
    class Meta:
        table = 'mailings'
        ordering = ['id']
        
    id = fields.BigIntField(pk=True)
    post = fields.ForeignKeyField('models.Post', to_field='id')
    send_at = fields.DatetimeField()


class Post(Model):
    class Meta:
        table = 'static_content'

    id = fields.BigIntField(pk=True)
    text = fields.TextField(null=True)
    photo_file_id = fields.CharField(max_length=256, null=True)
    video_file_id = fields.CharField(max_length=256, null=True)
    video_note_id = fields.CharField(max_length=256, null=True)
    document_file_id = fields.CharField(max_length=256, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
