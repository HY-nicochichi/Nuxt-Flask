from json import dumps
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import decode_token
from models import User
from . import (
    app,
    client,
    password,
    user,
    headers
)

JWT_API_ROUTE: str = '/jwt/'

class TestJwtPost:
    def test_Content_Typeが正しくない場合は415エラーになること(
        self, client: FlaskClient, password: str, user: User
    ) -> None:
        resp = client.post(
            JWT_API_ROUTE,
            data = dumps({
                'email': user.email,
                'password': password
            })
        )
        assert resp.status_code == 415
        assert resp.get_json()['msg'] == 'Invalid Content-Type header'

    def test_JSONの構文が不正な場合は400エラーになること(
        self, client: FlaskClient, headers: dict[str, str]
    ) -> None:
        resp = client.post(
            JWT_API_ROUTE,
            headers = headers,
            data = 'invalid'
        )
        assert resp.status_code == 400
        assert resp.get_json()['msg'] == 'Invalid JSON body syntax'

    def test_バリデーションエラーの場合は422エラーになること(
        self, client: FlaskClient, user: User, headers: dict[str, str]
    ) -> None:
        resp = client.post(
            JWT_API_ROUTE,
            headers = headers,
            data = dumps({
                'email': user.email,
                'password': 'invalid'
            })
        )
        assert resp.status_code == 422
        assert resp.get_json()['validation_failure'][0]['loc'] == ['password']

    def test_存在しないメールアドレスの場合は401エラーになること(
        self, client: FlaskClient, password: str, headers: dict[str, str]
    ) -> None:
        resp = client.post(
            JWT_API_ROUTE,
            headers = headers,
            data = dumps({
                'email': 'jiro@email.com',
                'password': password
            })
        )
        assert resp.status_code == 401
        assert resp.get_json()['msg'] == 'Invalid email or password'

    def test_パスワードが間違っている場合は401エラーになること(
        self, client: FlaskClient, user: User, headers: dict[str, str]
    ) -> None:
        resp = client.post(
            JWT_API_ROUTE,
            headers = headers,
            data = dumps({
                'email': user.email,
                'password': 'Jiro1234'
            })
        )
        assert resp.status_code == 401
        assert resp.get_json()['msg'] == 'Invalid email or password'

    def test_正しい認証情報でアクセストークンが発行されること(
        self, app: Flask, client: FlaskClient, password: str, user: User, headers: dict[str, str]
    ) -> None:
        resp = client.post(
            JWT_API_ROUTE,
            headers = headers,
            data = dumps({
                'email': user.email,
                'password': password
            })
        )
        assert resp.status_code == 200
        with app.app_context():
            access_token: str = resp.get_json()['access_token']
            assert decode_token(access_token)['sub'] == user.id
