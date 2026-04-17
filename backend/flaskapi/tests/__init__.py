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

def isolated_test_env(func: Callable) -> Callable:
    @wraps(func)
    def decorated(*args, **kwargs) -> None:
        with app.app_context():
            db_orm.create_all()
            func(*args, **kwargs)
            db_orm.session.remove()
            db_orm.drop_all()
    return staticmethod(decorated)

def create_db_data(model: type[AppModel], **kwargs) -> AppModel:
    with db_transaction():
        instance: AppModel = model.create(**kwargs)
    db_orm.session.refresh(instance)
    return instance

user_data: dict[str, str] = {
    'email': 'taro@email.com',
    'password': 'Taro1234',
    'name': 'Taro'
}

def auth_header(id: UUID) -> dict[str, str]:
    return {'Authorization': f'Bearer {create_access_token(str(id))}'}

json_header: dict[str, str] = {'Content-Type': 'application/json'}
