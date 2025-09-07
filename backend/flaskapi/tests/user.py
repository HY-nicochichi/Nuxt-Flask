from time import sleep
from uuid import uuid4
from json import dumps
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from models import User
from tests import (
    app,
    client,
    password,
    user,
    headers
)

USER_API_ROUTE = '/user/'

def test_user_get(app: Flask, client: FlaskClient, user: User) -> None:
    bad_id = str(uuid4())
    with app.app_context():
        bad_jwt: str = create_access_token(bad_id)
        good_jwt: str = create_access_token(user.id)
    
    bad_resp1 = client.get(USER_API_ROUTE)
    assert bad_resp1.status_code == 401
    assert bad_resp1.get_json()['msg'] == 'Missing Authorization Header'
    
    bad_resp2 = client.get(
        USER_API_ROUTE,
        headers = {'Authorization': f'Bearer {bad_jwt}'}
    )
    assert bad_resp2.status_code == 401
    assert bad_resp2.get_json()['msg'] == f'Error loading the user {bad_id}'
    
    good_resp = client.get(
        USER_API_ROUTE,
        headers = {'Authorization': f'Bearer {good_jwt}'}
    )
    assert good_resp.status_code == 200
    assert 'email' in good_resp.get_json()
    assert 'name' in good_resp.get_json()
    
    sleep(7.0)
    bad_resp3 = client.get(
        USER_API_ROUTE,
        headers = {'Authorization': f'Bearer {good_jwt}'}
    )
    assert bad_resp3.status_code == 401
    assert bad_resp3.get_json()['msg'] == 'Token has expired'

def test_user_post(client: FlaskClient, user: User, headers: dict[str, str]) -> None:
    bad_resp = client.post(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'email': user.email,
            'password': 'Jiro1234',
            'name': 'Jiro'
        })
    )
    assert bad_resp.status_code == 409
    assert bad_resp.get_json()['msg'] == 'Email already taken'

    good_resp = client.post(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'email': 'jiro@email.com',
            'password': 'Jiro1234',
            'name': 'Jiro'
        })
    )
    assert good_resp.status_code == 200
    assert good_resp.get_json()['msg'] == 'Success'

def test_user_put(
    client: FlaskClient, password: str, user: User, headers: dict[str, str]
) -> None:
    bad_resp1 = client.put(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'param': 'email',
            'current_val': 'jiro@email.com',
            'new_val': 'jiro@email.com'
        })
    )
    assert bad_resp1.status_code == 400
    assert bad_resp1.get_json()['msg'] == 'Invalid current value'
   
    bad_resp2 = client.put(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'param': 'email',
            'current_val': user.email,
            'new_val': user.email
        })
    )
    assert bad_resp2.status_code == 409
    assert bad_resp2.get_json()['msg'] == 'New value already taken'
    
    good_resp1 = client.put(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'param': 'email',
            'current_val': user.email,
            'new_val': 'jiro@email.com'
        })
    )
    assert good_resp1.status_code == 200
    assert good_resp1.get_json()['msg'] == 'Success'
    
    bad_resp3 = client.put(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'param': 'password',
            'current_val': 'Jiro1234',
            'new_val': 'Jiro1234'
        })
    )
    assert bad_resp3.status_code == 400
    assert bad_resp3.get_json()['msg'] == 'Invalid current value'
    
    good_resp2 = client.put(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'param': 'password',
            'current_val': password,
            'new_val': 'Jiro1234'
        })
    )
    assert good_resp2.status_code == 200
    assert good_resp2.get_json()['msg'] == 'Success'
    
    good_resp3 = client.put(
        USER_API_ROUTE,
        headers = headers,
        data = dumps({
            'param': 'name',
            'current_val': user.name,
            'new_val': 'Jiro'
        })
    )
    assert good_resp3.status_code == 200
    assert good_resp3.get_json()['msg'] == 'Success'

def test_user_delete(client: FlaskClient, headers: dict[str, str]) -> None:
    good_resp = client.delete(
        USER_API_ROUTE,
        headers = headers
    )
    assert good_resp.status_code == 200
    assert good_resp.get_json()['msg'] == 'Success'
