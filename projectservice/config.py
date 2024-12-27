import os
import errno
from typing import Optional
from contextvars import ContextVar
from logging.config import dictConfig
from logging import Filter, LogRecord

from pydantic_settings import  BaseSettings
from pydantic import BaseModel


class Settings(BaseSettings):
    db_user: str
    db_pwd: str
    db_host: str
    db_port: str
    db_name: str
    debug: bool = False
    auth_token_url: str
    auth_schema: str
    auth_url: str
    auth_jwks: str
    auth_issuer: str
    auth_audience: str
    azure_instrument_key: str
    allowed_groups: str

    class Config:
        env_file = '.env'


settings = Settings()
x_user_id: ContextVar[Optional[str]] = ContextVar('x_user_id', default=None)


class UserIdFilter(Filter):
    def __init__(self, name: str = ''):
        super().__init__(name=name)

    def filter(self, record: LogRecord) -> bool:
        """
        Attach a User ID to the log record.
        """

        record.x_user_id = x_user_id.get()
        return True

