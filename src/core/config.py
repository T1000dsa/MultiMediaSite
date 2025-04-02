# main settings (Db settings, logging, pydantic settings etc)
from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

import os
import logging 

logger = logging.getLogger(__name__)

logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port:int=8000


class Api_current_Prefix(BaseModel):
    prefix:str='/v1'
    users:str='/users'


class ApiPrefix(BaseModel):
    prefix:str='/api'
    current:Api_current_Prefix = Api_current_Prefix()


class DatabaseConfig(BaseModel):
    url:PostgresDsn
    echo:bool=True
    echo_pool:bool=False
    pool_size:int=5
    max_overflow:int=10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        env_prefix='FAST__',
        env_file='.env',  # ('.env', '.env.template')
        env_file_encoding='utf-8'
    )
    run: RunConfig = RunConfig()
    api_prefix: ApiPrefix = ApiPrefix()
    db: DatabaseConfig

settings = Settings()
print(settings)