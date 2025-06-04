from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path 
from fastapi.templating import Jinja2Templates
import os

from src.core.config.models import (
    RunConfig, 
    Current_ApiPrefix,
    Mode, 
    DatabaseConfig, 
    RedisSettings, 
    Email_Settings,
    Title
    )


base_dir = Path(__file__).parent.parent.parent
media_root = base_dir / 'media'
default_picture_none =  '/media/Not_exist.png'
frontend_root = base_dir / 'frontend' / 'templates'
max_file_size = 10 * 1024**2 # 10 mb

templates = Jinja2Templates(directory=frontend_root)


os.makedirs(media_root, exist_ok=True)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_prefix='FAST__',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Run config
    title:Title
    run: RunConfig
    prefix: Current_ApiPrefix = Current_ApiPrefix()
    mode: Mode

    # Services
    db: DatabaseConfig
    redis: RedisSettings
    email:Email_Settings

    # API
    #...

    #elastic:ElasticSearch = ElasticSearch()

    def is_prod(self):
        if self.mode.mode == 'PROD':
            return True
        return False

settings = Settings()
if settings.mode.mode not in ('DEV', 'TEST'):
    raise Exception('mode should be DEV or TEST')

auth_prefix = '/users'
main_prefix = settings.prefix.api_data.prefix