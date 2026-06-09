from typing import Any, Literal
from os import environ
from datetime import timedelta

class Config:
    JWT_SECRET_KEY: str = environ['JWT_SECRET_KEY']
    ORM_ENGINE_OPTIONS: dict[str, Any] = {
        'pool_size': int(environ['APP_CONCURRENCY']),
        'max_overflow': 0,
        'pool_timeout': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

class ServerAppConfig(Config):
    ORM_ENGINE_URL: str = environ['ORM_ENGINE_URL']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15.0)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14.0)

class TestAppConfig(Config):
    TESTING: bool = True
    ORM_ENGINE_URL: str = f'{environ['ORM_ENGINE_URL']}_test'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3.0)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=1.0)

type Mode = Literal['server', 'test']

configs: dict[Mode, Config] = {
    'server': ServerAppConfig(), 'test': TestAppConfig()
}
