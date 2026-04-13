from json import dumps
from flask_jwt_extended import decode_token
from models import User
from . import (
    app,
    client,
    db_cleaned,
    create_db_data,
    user_data,
    json_header
)

JWT_ROUTE: str = '/jwt/'

class TestJwtPost:
    @db_cleaned
    def test_Invalid_Content_Type_header_415() -> None:
        resp = client.post(
            JWT_ROUTE,
            data=dumps({'email': user_data['email'], 'password': user_data['password']})
        )
        assert resp.status_code == 415
        assert resp.get_json() == {'msg': 'Invalid Content-Type header'}

    @db_cleaned
    def test_Invalid_JSON_body_syntax_400() -> None:
        resp = client.post(
            JWT_ROUTE, headers=json_header, data='Invalid JSON'
        )
        assert resp.status_code == 400
        assert resp.get_json() == {'msg': 'Invalid JSON body syntax'}

    @db_cleaned
    def test_Validation_failure_422() -> None:
        resp = client.post(
            JWT_ROUTE,
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

    @db_cleaned
    def test_Invalid_email_401() -> None:
        resp = client.post(
            JWT_ROUTE,
            headers=json_header,
            data=dumps({'email': user_data['email'], 'password': user_data['password']})
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Invalid email or password'}

    @db_cleaned
    def test_Invalid_password_401() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.post(
            JWT_ROUTE,
            headers=json_header,
            data=dumps({'email': user.email, 'password': 'WrongPassword1234'})
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Invalid email or password'}

    @db_cleaned
    def test_Access_token_created_200() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.post(
            JWT_ROUTE,
            headers=json_header,
            data=dumps({'email': user.email, 'password': user_data['password']})
        )
        assert resp.status_code == 200
        with app.app_context():
            access_token: str = resp.get_json()['access_token']
            assert decode_token(access_token)['sub'] == str(user.id)
