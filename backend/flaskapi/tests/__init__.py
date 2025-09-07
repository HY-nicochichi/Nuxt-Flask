from typing import (
    Generator,
    Any
)
from datetime import timedelta
from pytest import fixture
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from models import User
from views import bps
from extensions import (
    db_orm,
    jwt_manager,
    cross_origin
)

@fixture(scope='function')
def app() -> Generator[Flask, Any, None]:
    app = Flask('test')

    app.config.from_pyfile('/flaskapi/settings.py')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=7.0)

    for bp in bps:
        app.register_blueprint(bp)

    db_orm.init_app(app)
    jwt_manager.init_app(app)
    cross_origin.init_app(app)

    with app.app_context():
        db_orm.create_all()

    yield app

    with app.app_context():
        db_orm.session.remove()
        db_orm.drop_all()

@fixture(scope='function')
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@fixture(scope='function')
def password() -> str:
    return 'Taro1234'

@fixture(scope='function')
def user(app: Flask, password: str) -> User:
    with app.app_context():
        user = User.create('taro@email.com', password, 'Taro')
        db_orm.session.refresh(user)
    return user

@fixture(scope='function')
def headers(app: Flask, user: User) -> dict[str, str]:
    with app.app_context():
        return {
            'Authorization': f'Bearer {create_access_token(user.id)}',
            'Content-Type': 'application/json'
        }
