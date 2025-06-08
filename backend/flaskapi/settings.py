from os import getenv
from datetime import timedelta

match getenv('APP_RUN_MODE'):
    case 'production':
        SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': int(getenv('APP_CONCURRENCY')),
            'max_overflow': 0,
            'pool_timeout': 5,
            'pool_recycle': 300,
            'pool_pre_ping': False,
            'connect_args': {
                'options': '-c statement_timeout=5000'
            }
        }
        SQLALCHEMY_ECHO = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7.0)
    case 'test':
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_ECHO = False
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        JWT_SECRET_KEY = 'test-secret'
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3.0)
