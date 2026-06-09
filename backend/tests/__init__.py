from uuid import UUID
from collections.abc import Callable
from functools import wraps
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token, create_refresh_token
from src.models import AppModel, db_transaction
from src.core import create_app
from src.extensions import orm

app: Flask = create_app(mode='test')
client: FlaskClient = app.test_client()

def isolated_test_env(func: Callable) -> Callable:
    @wraps(func)
    def decorated(*args, **kwargs) -> None:
        with app.app_context():
            try:
                AppModel.metadata.create_all(bind=orm.engine)
                func(*args, **kwargs)
            finally:
                orm.remove_session()
                AppModel.metadata.drop_all(bind=orm.engine)
    return staticmethod(decorated)

def create_db_data[T: AppModel](model: type[T], **kwargs) -> T:
    with db_transaction():
        instance: T = model.create(**kwargs)
    orm.session.refresh(instance)
    return instance

user_data: dict[str, str] = {
    'email': 'taro@email.com', 'password': 'Taro1234', 'name': 'Taro'
}

def auth_header(id: UUID, refresh: bool = False) -> dict[str, str]:
    token: str = create_refresh_token(str(id)) if refresh else create_access_token(str(id))
    return {'Authorization': f'Bearer {token}'}

json_header: dict[str, str] = {'Content-Type': 'application/json'}
