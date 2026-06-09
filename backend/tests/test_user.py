from typing import cast
from time import sleep
from uuid import uuid7
from json import dumps
from werkzeug.test import TestResponse
from src.models.user import User
from tests import (
    isolated_test_env, create_db_data, auth_header,
    client, user_data, json_header
)

USER_ROUTE: str = '/users'

class TestCreateUser:
    @isolated_test_env
    def test_Email_already_taken_409() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.post(
            USER_ROUTE,
            headers=json_header,
            data=dumps({
                'email': user.email, 'password': 'Jiro1234', 'name': 'Jiro'
            })
        )
        assert resp.status_code == 409
        assert resp.get_json() == {'msg': 'Email already taken'}

    @isolated_test_env
    def test_Create_user_204() -> None:
        resp: TestResponse = client.post(
            USER_ROUTE, headers=json_header, data=dumps(user_data)
        )
        assert resp.status_code == 204
        user: User = User.all()[0]
        assert user.to_dict(include={'email', 'name'}) == {
            'email': user_data['email'], 'name': user_data['name']
        } and user.check_password(user_data['password'])

class TestGetMe:
    @isolated_test_env
    def test_Missing_Authorization_header_401() -> None:
        resp: TestResponse = client.get(f'{USER_ROUTE}/me')
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Missing Authorization Header'}

    @isolated_test_env
    def test_Error_loading_user_401() -> None:
        bad_id = uuid7()
        resp: TestResponse = client.get(
            f'{USER_ROUTE}/me', headers=auth_header(bad_id)
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': f'Error loading the user {bad_id}'}

    @isolated_test_env
    def test_Get_me_200() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.get(
            f'{USER_ROUTE}/me', headers=auth_header(user.id)
        )
        assert resp.status_code == 200
        assert resp.get_json() == user.to_dict(include={'email', 'name'})

    @isolated_test_env
    def test_Token_has_expired_401() -> None:
        user: User = create_db_data(User, **user_data)
        expired_auth_header = auth_header(user.id)
        sleep(3.0)
        resp: TestResponse = client.get(
            f'{USER_ROUTE}/me', headers=expired_auth_header
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Token has expired'}

class TestUpdateMe:
    @isolated_test_env
    def test_No_params_to_update_422() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.patch(
            f'{USER_ROUTE}/me',
            headers=auth_header(user.id)|json_header,
            data=dumps({'current_password': user_data['password']})
        )
        assert resp.status_code == 422
        assert resp.get_json() == {'msg': 'No params to update'}

    @isolated_test_env
    def test_Invalid_current_password_422() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.patch(
            f'{USER_ROUTE}/me',
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'current_password': 'WrongPassword1234', 'email': 'new-taro@email.com'
            })
        )
        assert resp.status_code == 422
        assert resp.get_json() == {'msg': 'Invalid current password'}

    @isolated_test_env
    def test_Email_already_taken_409() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.patch(
            f'{USER_ROUTE}/me',
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'current_password': user_data['password'], 'email': user.email
            })
        )
        assert resp.status_code == 409
        assert resp.get_json() == {'msg': 'Email already taken'}

    @isolated_test_env
    def test_Update_me_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.patch(
            f'{USER_ROUTE}/me',
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'current_password': user_data['password'],
                'email': 'new-taro@email.com',
                'password': 'NewTaro1234',
                'name': 'New Taro'
            })
        )
        assert resp.status_code == 204
        user = cast(User, User.find_by(id=user.id))
        assert user.to_dict(include={'email', 'name'}) == {
            'email': 'new-taro@email.com', 'name': 'New Taro'
        } and user.check_password('NewTaro1234')

class TestDeleteMe:
    @isolated_test_env
    def test_Delete_me_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.delete(
            f'{USER_ROUTE}/me', headers=auth_header(user.id)
        )
        assert resp.status_code == 204
        assert User.find_by(id=user.id) is None
