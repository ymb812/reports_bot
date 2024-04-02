from pydantic import BaseModel, SecretStr, fields
from pydantic_settings import SettingsConfigDict


class BotSettings(BaseModel):
    bot_token: SecretStr = fields.Field(max_length=100, alias='TELEGRAM_BOT_TOKEN')
    bot_link: str = fields.Field(max_length=100, alias='BOT_BASE_LINK')
    admin_password: SecretStr = fields.Field(max_length=100, alias='ADMIN_PASSWORD')
    admin_chat_id: str = fields.Field(alias='ADMIN_CHAT_ID')
    admin_chat_link: str = fields.Field(alias='ADMIN_CHAT_LINK')
    required_channel_id: str = fields.Field(alias='REQUIRED_CHANNEL_ID')
    welcome_post_id: int = fields.Field(alias='WELCOME_POST_ID')
    notification_post_id: int = fields.Field(alias='NOTIFICATION_POST_ID')
    registered_post_id: int = fields.Field(alias='REGISTERED_POST_ID')


class Dialogues(BaseModel):
    items_per_page_height: int = fields.Field(alias='CATEGORIES_HEIGHT')
    items_per_page_width: int = fields.Field(alias='CATEGORIES_WIDTH')


class Broadcaster(BaseModel):
    mailing_batch_size: int = fields.Field(alias='MAILING_BATCH_SIZE', default=25)
    broadcaster_sleep: int = fields.Field(alias='BROADCASTER_SLEEP', default=1)
    notification_hours: int = fields.Field(alias='NOTIFICATION_HOURS', default=10)
    notification_minutes: int = fields.Field(alias='NOTIFICATION_MINUTES', default=0)


class AppSettings(BaseModel):
    prod_mode: bool = fields.Field(alias='PROD_MODE', default=False)
    excel_file: str = fields.Field(alias='EXCEL_FILE', default='Users stats.xlsx')
    stop_list_json_file: str = fields.Field(alias='STOP_LIST_JSON_FILE', default='stop_list.json')
    base_files_dir: str = fields.Field(alias='BASE_FILES_DIR', default='files_from_server')
    remote_directory: str = fields.Field(alias='SERVER_FILES_DIR')


class PostgresSettings(BaseModel):
    db_user: str = fields.Field(alias='POSTGRES_USER')
    db_host: str = fields.Field(alias='POSTGRES_HOST')
    db_port: int = fields.Field(alias='POSTGRES_PORT')
    db_pass: SecretStr = fields.Field(alias='POSTGRES_PASSWORD')
    db_name: SecretStr = fields.Field(alias='POSTGRES_DATABASE')


class RedisSettings(BaseModel):
    redis_host: str = fields.Field(alias='REDIS_HOST')
    redis_port: int = fields.Field(alias='REDIS_PORT')
    redis_name: str = fields.Field(alias='REDIS_NAME')


class FTPSettings(BaseModel):
    ftp_user: str = fields.Field(alias='FTP_USER')
    ftp_host: str = fields.Field(alias='FTP_HOST')
    ftp_port: int = fields.Field(alias='FTP_PORT')
    ftp_pass: SecretStr = fields.Field(alias='FTP_PASSWORD')


class Settings(
    BotSettings,
    AppSettings,
    PostgresSettings,
    Broadcaster,
    Dialogues,
    RedisSettings,
    FTPSettings
):
    model_config = SettingsConfigDict(extra='ignore')
