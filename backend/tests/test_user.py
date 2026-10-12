from typing import cast
from time import sleep
from uuid import uuid7
from json import dumps
from werkzeug.test import TestResponse
from src.models import Q
from src.models.user import User
from src.routers.user import USER_ROUTE
from tests import (
    isolated_test_env, create_db_data, auth_header,
    client, user_data, json_header
)

class TestCreateUser:
    @isolated_test_env
    def test_Email_already_taken_409() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.post(
            USER_ROUTE,
            headers=json_header,
            data=dumps({
                'email': user.email, 'password': 'JiroPassword123', 'name': 'Jiro'
            })
        )
        assert resp.status_code == 409
        assert resp.get_json() == {'msg': 'Email already taken'}

    @isolated_test_env
    def test_Create_user_201() -> None:
        resp1: TestResponse = client.post(
            USER_ROUTE, headers=json_header, data=dumps(user_data)
        )
        resp2: TestResponse = client.post(
            USER_ROUTE, headers=json_header, data=dumps({
                'email': 'JIRO@email.com', 'password': 'JiroPassword123', 'name': 'Jiro'
            })
        )
        for resp in [resp1, resp2]:
            assert resp.status_code == 201
            assert resp.headers['Location'] == f'{USER_ROUTE}/me'
        [user1, user2] = User.all(Q.order_by(User.created))
        assert user1.to_dict(include={'email', 'name'}) == {
            'email': user_data['email'], 'name': user_data['name']
        } and user1.check_password(user_data['password'])
        assert user2.to_dict(include={'email', 'name'}) == {
            'email': 'jiro@email.com', 'name': 'Jiro'
        } and user2.check_password('JiroPassword123')

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
                'current_password': 'WrongPassword123', 'email': 'new-taro@email.com'
            })
        )
        assert resp.status_code == 422
        assert resp.get_json() == {'msg': 'Invalid current password'}

    @isolated_test_env
    def test_Email_already_taken_409() -> None:
        user1: User = create_db_data(User, **user_data)
        user2: User = create_db_data(
            User, email='jiro@email.com', password='JiroPassword123', name='Jiro'
        )
        resp: TestResponse = client.patch(
            f'{USER_ROUTE}/me',
            headers=auth_header(user1.id)|json_header,
            data=dumps({
                'current_password': user_data['password'], 'email': user2.email
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
                'password': 'NewTaroPassword123',
                'name': 'New Taro'
            })
        )
        assert resp.status_code == 204
        user = cast(User, User.find_by(id=user.id))
        assert user.to_dict(include={'email', 'name'}) == {
            'email': 'new-taro@email.com', 'name': 'New Taro'
        } and user.check_password('NewTaroPassword123')

class TestDeleteMe:
    @isolated_test_env
    def test_Delete_me_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp: TestResponse = client.delete(
            f'{USER_ROUTE}/me', headers=auth_header(user.id)
        )
        assert resp.status_code == 204
        assert User.find_by(id=user.id) is None
