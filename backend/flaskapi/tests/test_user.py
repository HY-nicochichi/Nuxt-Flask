from time import sleep
from uuid import uuid4
from json import dumps
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from models import User
from . import (
    app,
    client,
    password,
    user,
    headers
)

USER_API_ROUTE: str = '/user/'

class TestUserGet:
    def test_未ログイン時は401エラーになること(
        self, client: FlaskClient
    ) -> None:
        resp = client.get(USER_API_ROUTE)
        assert resp.status_code == 401
        assert resp.get_json()['msg'] == 'Missing Authorization Header'
  
    def test_存在しないユーザーのトークンの場合は401エラーになること(
        self, app: Flask, client: FlaskClient
    ) -> None:
        bad_id: str = str(uuid4())
        with app.app_context():
            bad_jwt: str = create_access_token(bad_id)
        resp = client.get(
            USER_API_ROUTE,
            headers = {'Authorization': f'Bearer {bad_jwt}'}
        )
        assert resp.status_code == 401
        assert resp.get_json()['msg'] == f'Error loading the user {bad_id}'

    def test_正しいトークンでユーザー情報を取得できること(
        self, app: Flask, client: FlaskClient, user: User
    ) -> None:
        with app.app_context():
            good_jwt: str = create_access_token(user.id)
        resp = client.get(
            USER_API_ROUTE,
            headers = {'Authorization': f'Bearer {good_jwt}'}
        )
        assert resp.status_code == 200
        assert resp.get_json()['email'] == user.email
        assert resp.get_json()['name'] == user.name

    def test_有効期限が切れたトークンの場合は401エラーになること(
        self, app: Flask, client: FlaskClient, user: User
    ) -> None:
        with app.app_context():
            good_jwt: str = create_access_token(user.id)
        sleep(3.0)
        resp = client.get(
            USER_API_ROUTE,
            headers = {'Authorization': f'Bearer {good_jwt}'}
        )
        assert resp.status_code == 401
        assert resp.get_json()['msg'] == 'Token has expired'

class TestUserPost:
    def test_既に登録済みのメールアドレスの場合は409エラーになること(
        self, client: FlaskClient, user: User, headers: dict[str, str]
    ) -> None:
        resp = client.post(
            USER_API_ROUTE,
            headers = headers,
            data = dumps({
                'email': user.email,
                'password': 'Jiro1234',
                'name': 'Jiro'
            })
        )
        assert resp.status_code == 409
        assert resp.get_json()['msg'] == 'Email already taken'

    def test_新しいメールアドレスなら201で登録成功すること(
        self, client: FlaskClient, headers: dict[str, str]
    ) -> None:
        resp = client.post(
            USER_API_ROUTE,
            headers = headers,
            data = dumps({
                'email': 'jiro@email.com',
                'password': 'Jiro1234',
                'name': 'Jiro'
            })
        )
        assert resp.status_code == 201
        assert 'id' in resp.get_json()

class TestUserPatch:
    def test_現在の値が正しくない場合は400エラーになること(
        self, client: FlaskClient, headers: dict[str, str]
    ) -> None:
        resp = client.patch(
            USER_API_ROUTE,
            headers = headers,
            data = dumps({
                'param': 'email',
                'current_val': 'jiro@email.com',
                'new_val': 'jiro@email.com'
            })
        )
        assert resp.status_code == 400
        assert resp.get_json()['msg'] == 'Invalid current value'

    def test_新しい値が既に使われている場合は409エラーになること(
        self, client: FlaskClient, user: User, headers: dict[str, str]
    ) -> None:
        resp = client.patch(
            USER_API_ROUTE,
            headers = headers,
            data = dumps({
                'param': 'email',
                'current_val': user.email,
                'new_val': user.email
            })
        )
        assert resp.status_code == 409
        assert resp.get_json()['msg'] == 'New value already taken'

    def test_メールアドレスの変更ができること(
        self, client: FlaskClient, user: User, headers: dict[str, str]
    ) -> None:
        resp = client.patch(
            USER_API_ROUTE,
            headers = headers,
            data = dumps({
                'param': 'email',
                'current_val': user.email,
                'new_val': 'jiro@email.com'
            })
        )
        assert resp.status_code == 204

    def test_パスワードの変更ができること(
        self, client: FlaskClient, password: str, headers: dict[str, str]
    ) -> None:
        resp = client.patch(
            USER_API_ROUTE,
            headers = headers,
            data = dumps({
                'param': 'password',
                'current_val': password,
                'new_val': 'Jiro1234'
            })
        )
        assert resp.status_code == 204

    def test_名前の変更ができること(
        self, client: FlaskClient, user: User, headers: dict[str, str]
    ) -> None:
        resp = client.patch(
            USER_API_ROUTE,
            headers = headers,
            data = dumps({
                'param': 'name',
                'current_val': user.name,
                'new_val': 'Jiro'
            })
        )
        assert resp.status_code == 204

class TestUserDelete:
    def test_ユーザーを削除できること(
        self, client: FlaskClient, headers: dict[str, str]
    ) -> None:
        resp = client.delete(
            USER_API_ROUTE,
            headers = headers
        )
        assert resp.status_code == 204
