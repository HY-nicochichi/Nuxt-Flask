from uuid import UUID
from collections.abc import Callable
from functools import wraps
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from views import bps
from extensions import (
    AppModel,
    db_orm,
    jwt_manager,
    cross_origin,
    db_transaction
)

app = Flask('test')

app.config.from_pyfile('settings.py')

for bp in bps:
    app.register_blueprint(bp)

db_orm.init_app(app)
jwt_manager.init_app(app)
cross_origin.init_app(app)

client: FlaskClient = app.test_client()

def db_cleaned(func: Callable) -> Callable:
    @wraps(func)
    def decorated(*args, **kwargs) -> None:
        with app.app_context():
            db_orm.drop_all()
            db_orm.create_all()
        func(*args, **kwargs)
    return staticmethod(decorated)

def create_db_data(model: type[AppModel], **kwargs) -> AppModel:
    with app.app_context():
        with db_transaction():
            instance: AppModel = model.create(**kwargs)
        db_orm.session.refresh(instance)
        db_orm.session.expunge(instance)
        db_orm.session.remove()
    return instance

user_data: dict[str, str] = {
    'email': 'taro@email.com',
    'password': 'Taro1234',
    'name': 'Taro'
}

def auth_header(id: UUID) -> dict[str, str]:
    with app.app_context():
        return {'Authorization': f'Bearer {create_access_token(str(id))}'}

json_header: dict[str, str] = {'Content-Type': 'application/json'}
