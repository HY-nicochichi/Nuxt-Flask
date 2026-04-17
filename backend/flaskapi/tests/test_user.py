from time import sleep
from uuid import uuid7
from json import dumps
from models import User
from . import (
    client,
    isolated_test_env,
    create_db_data,
    user_data,
    auth_header,
    json_header
)

USER_ROUTE: str = '/user/'

class TestUserGet:
    @isolated_test_env
    def test_Missing_Authorization_header_401() -> None:
        resp = client.get(USER_ROUTE)
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Missing Authorization Header'}

    @isolated_test_env
    def test_Error_loading_user_401() -> None:
        bad_id = uuid7()
        resp = client.get(
            USER_ROUTE, headers=auth_header(bad_id)
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': f'Error loading the user {bad_id}'}

    @isolated_test_env
    def test_Get_user_info_200() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.get(
            USER_ROUTE, headers=auth_header(user.id)
        )
        assert resp.status_code == 200
        assert resp.get_json() == {'email': user.email, 'name': user.name}

    @isolated_test_env
    def test_Token_has_expired_401() -> None:
        user: User = create_db_data(User, **user_data)
        expired_auth_header = auth_header(user.id)
        sleep(3.0)
        resp = client.get(
            USER_ROUTE, headers=expired_auth_header
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Token has expired'}

class TestUserPost:
    @isolated_test_env
    def test_Email_already_taken_409() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.post(
            USER_ROUTE,
            headers=json_header,
            data=dumps({
                'email': user.email, 'password': 'Jiro1234', 'name': 'Jiro'
            })
        )
        assert resp.status_code == 409
        assert resp.get_json() == {'msg': 'Email already taken'}

    @isolated_test_env
    def test_User_created_204() -> None:
        resp = client.post(
            USER_ROUTE, headers=json_header, data=dumps(user_data)
        )
        assert resp.status_code == 204
        assert len(User.all()) == 1

class TestUserPatch:
    @isolated_test_env
    def test_No_params_to_update_422() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({'current_password': user_data['password']})
        )
        assert resp.status_code == 422
        assert resp.get_json() == {'msg': 'No params to update'}

    @isolated_test_env
    def test_Invalid_current_password_422() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
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
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'current_password': user_data['password'], 'email': user.email
            })
        )
        assert resp.status_code == 409
        assert resp.get_json() == {'msg': 'Email already taken'}

    @isolated_test_env
    def test_User_updated_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'current_password': user_data['password'],
                'email': 'new-taro@email.com',
                'password': 'NewTaro1234',
                'name': 'New Taro'
            })
        )
        assert resp.status_code == 204
        updated_user: User = User.find_by(id=user.id)
        assert updated_user.email == 'new-taro@email.com'
        assert updated_user.is_password_matched('NewTaro1234')
        assert updated_user.name == 'New Taro'

class TestUserDelete:
    @isolated_test_env
    def test_User_deleted_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.delete(
            USER_ROUTE, headers=auth_header(user.id)
        )
        assert resp.status_code == 204
        assert len(User.all()) == 0
