from os import getenv
from datetime import timedelta

SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7.0)
