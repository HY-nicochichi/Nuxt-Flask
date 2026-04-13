from time import sleep
from uuid import uuid7
from json import dumps
from models import User
from . import (
    app,
    client,
    db_cleaned,
    create_db_data,
    user_data,
    auth_header,
    json_header
)

USER_ROUTE: str = '/user/'

class TestUserGet:
    @db_cleaned
    def test_Missing_Authorization_header_401() -> None:
        resp = client.get(USER_ROUTE)
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': 'Missing Authorization Header'}

    @db_cleaned
    def test_Error_loading_user_401() -> None:
        bad_id = uuid7()
        resp = client.get(
            USER_ROUTE, headers=auth_header(bad_id)
        )
        assert resp.status_code == 401
        assert resp.get_json() == {'msg': f'Error loading the user {bad_id}'}

    @db_cleaned
    def test_Get_user_info_200() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.get(
            USER_ROUTE, headers=auth_header(user.id)
        )
        assert resp.status_code == 200
        assert resp.get_json() == {'email': user.email, 'name': user.name}

    @db_cleaned
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
    @db_cleaned
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

    @db_cleaned
    def test_User_created_204() -> None:
        resp = client.post(
            USER_ROUTE, headers=json_header, data=dumps(user_data)
        )
        assert resp.status_code == 204
        with app.app_context():
            assert len(User.all()) == 1

class TestUserPatch:
    @db_cleaned
    def test_Invalid_current_value_422() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'param': 'email',
                'current_val': 'jiro@email.com',
                'new_val': 'jiro@email.com'
            })
        )
        assert resp.status_code == 422
        assert resp.get_json() == {'msg': 'Invalid current value'}

    @db_cleaned
    def test_New_value_already_taken_409() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'param': 'email',
                'current_val': user.email,
                'new_val': user.email
            })
        )
        assert resp.status_code == 409
        assert resp.get_json() == {'msg': 'New value already taken'}

    @db_cleaned
    def test_Email_updated_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'param': 'email',
                'current_val': user.email,
                'new_val': 'jiro@email.com'
            })
        )
        assert resp.status_code == 204

    @db_cleaned
    def test_Password_updated_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'param': 'password',
                'current_val': user_data['password'],
                'new_val': 'Jiro1234'
            })
        )
        assert resp.status_code == 204

    @db_cleaned
    def test_Name_updated_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.patch(
            USER_ROUTE,
            headers=auth_header(user.id)|json_header,
            data=dumps({
                'param': 'name',
                'current_val': user.name,
                'new_val': 'Jiro'
            })
        )
        assert resp.status_code == 204

class TestUserDelete:
    @db_cleaned
    def test_User_deleted_204() -> None:
        user: User = create_db_data(User, **user_data)
        resp = client.delete(
            USER_ROUTE, headers=auth_header(user.id)
        )
        assert resp.status_code == 204
        with app.app_context():
            assert len(User.all()) == 0
