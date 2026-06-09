from flask import Flask
from src.core import create_app
from src.models import AppModel
from src.extensions import orm

app: Flask = create_app(mode='server')

with app.app_context():
    AppModel.metadata.create_all(bind=orm.engine)
