from json import dumps
from werkzeug.test import TestResponse
from flask import current_app
from flask_jwt_extended import decode_token
from src.models.user import User
from src.routers.token import TOKEN_ROUTE
from tests import (
    isolated_test_env, create_db_data, auth_header,
    client, user_data, json_header
)

class TestCreateToken:
    @isolated_test_env
    def test_Unsupported_Media_Type_415() -> None:
        resp: TestResponse = client.post(
            TOKEN_ROUTE,
            data=dumps({'email': user_data['email'], 'password': user_data['password']})
        )
        assert resp.status_code == 415
        assert resp.get_json() == {'msg': 'Unsupported Media Type'}

    @isolated_test_env
    def test_Bad_Request_400() -> None:
        resp: TestResponse = client.post(
            TOKEN_ROUTE, headers=json_header, data='Invalid JSON'
        )
        assert resp.status_code == 400
        assert resp.get_json() == {'msg': 'Bad Request'}

    @isolated_test_env
    def test_Request_Entity_Too_Large_413() -> None:
        max_body_size: int = current_app.config['MAX_CONTENT_LENGTH']
        too_long_json: str = dumps({
            'key': 'A' * (max_body_size + 1 - len('{"key": ""}'))
        })
        resp: TestResponse = client.post(
            TOKEN_ROUTE, headers=json_header, data=too_long_json
        )
        assert resp.status_code == 413
        assert resp.get_json() == {'msg': 'Request Entity Too Large'}

    @isolated_test_env
    def test_Validation_failure_422() -> None:
        resp: TestResponse = client.post(
            TOKEN_ROUTE,
            headers=json_header,
            data=dumps({'email': user_data['email'], 'password': 'Invalid Password'})
        )
        assert resp.status_code == 422
        assert resp.get_json() == {
            'msg': 'Validation failed',
            'errors': [{
                'input': 'Invalid Password',
                'loc': ['password'],
                'msg': 'Password must be 15-75 characters and include letters and numbers'
            }]
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
            data=dumps({'email': user.email, 'password': 'WrongPassword123'})
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
