from json import dumps
from werkzeug.test import TestResponse
from flask_jwt_extended import decode_token
from src.models.user import User
from tests import (
    isolated_test_env, create_db_data, auth_header,
    client, user_data, json_header
)

TOKEN_ROUTE: str = '/tokens'

class TestCreateToken:
    @isolated_test_env
    def test_Invalid_Content_Type_header_415() -> None:
        resp: TestResponse = client.post(
            TOKEN_ROUTE,
            data=dumps({'email': user_data['email'], 'password': user_data['password']})
        )
        assert resp.status_code == 415
        assert resp.get_json() == {'msg': 'Invalid Content-Type header'}

    @isolated_test_env
    def test_Invalid_JSON_body_syntax_400() -> None:
        resp: TestResponse = client.post(
            TOKEN_ROUTE, headers=json_header, data='Invalid JSON'
        )
        assert resp.status_code == 400
        assert resp.get_json() == {'msg': 'Invalid JSON body syntax'}

    @isolated_test_env
    def test_Validation_failure_422() -> None:
        resp: TestResponse = client.post(
            TOKEN_ROUTE,
            headers=json_header,
            data=dumps({'email': user_data['email'], 'password': 'Invalid Password'})
        )
        assert resp.status_code == 422
        assert resp.get_json() == {
            'validation_failure': [
                {
                    'input': 'Invalid Password',
                    'loc': ['password'],
                    'msg': 'Password must be 8-20 characters and include uppercase, lowercase, and number'
                }
            ]
        }

    @isolated_test_env
    def test_Invalid_email_401() -> None:
        resp: TestResponse = client.post(
            TOKEN_ROUTE,
            headers=json_header,
            data=dumps({'email': user_data['email'], 'password': user_data['password']})
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Invalid email or password'}

    @isolated_test_env
    def test_Invalid_password_401() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.post(
            TOKEN_ROUTE,
            headers=json_header,
            data=dumps({'email': user.email, 'password': 'WrongPassword1234'})
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Invalid email or password'}

    @isolated_test_env
    def test_Create_token_200() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.post(
            TOKEN_ROUTE,
            headers=json_header,
            data=dumps({'email': user.email, 'password': user_data['password']})
        )
        assert resp.status_code == 200
        access_token: str = resp.get_json()['access_token']
        refresh_token: str = resp.get_json()['refresh_token']
        assert decode_token(access_token)['sub'] == str(user.id)
        assert decode_token(refresh_token)['sub'] == str(user.id)

class TestRefreshToken:
    @isolated_test_env
    def test_Refresh_token_200() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.post(
            f'{TOKEN_ROUTE}/refresh', headers=auth_header(user.id, refresh=True)
        )
        assert resp.status_code == 200
        access_token: str = resp.get_json()['access_token']
        assert decode_token(access_token)['sub'] == str(user.id)
