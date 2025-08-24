from datetime import timedelta
from uuid import uuid4
from pytest import fixture
from flask import Flask
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from models import User
from views import bps
from extensions import (
    db_orm,
    jwt_manager,
    cross_origin
)

@fixture(scope='function')
def app():
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

def sample_user(app: Flask) -> tuple[User, str]:
    password: str = 'Taro1234'
    user = User(
        id = str(uuid4()),
        email = 'taro@email.com',
        password_hash = generate_password_hash(password),
        name = 'Taro'
    )
    with app.app_context():
        db_orm.session.add(user)
        db_orm.session.commit()
        db_orm.session.refresh(user)
    return user, password

def sample_jwt(app: Flask, id: str) -> str:
    with app.app_context():
        jwt: str = create_access_token(identity=id)
    return jwt
