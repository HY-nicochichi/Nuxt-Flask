from time import sleep
from uuid import uuid4
from json import dumps
from flask import Flask
from . import (
    app,
    sample_jwt,
    sample_user
)

USER_API_ROUTE = '/user/'

def test_user_get(app: Flask) -> None:
    client = app.test_client()
    user, _ = sample_user(app)
    bad_id = str(uuid4())
    bad_jwt = sample_jwt(app, bad_id)
    good_jwt = sample_jwt(app, user.id)
    
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

def test_user_post(app: Flask) -> None:
    client = app.test_client()
    user, _ = sample_user(app)

    bad_resp = client.post(
        USER_API_ROUTE,
        headers = {'Content-Type': 'application/json'},
        data = dumps({
            'email': user.email,
            'password': 'Jiro123',
            'name': 'Jiro'
        })
    )
    assert bad_resp.status_code == 409
    assert bad_resp.get_json()['msg'] == 'Email already taken'

    good_resp = client.post(
        USER_API_ROUTE,
        headers = {'Content-Type': 'application/json'},
        data = dumps({
            'email': 'jiro@email.com',
            'password': 'Jiro123',
            'name': 'Jiro'
        })
    )
    assert good_resp.status_code == 200
    assert good_resp.get_json()['msg'] == 'Success'

def test_user_put(app: Flask) -> None:
    client = app.test_client()
    user, password = sample_user(app)
    jwt = sample_jwt(app, user.id)
    
    bad_resp1 = client.put(
        USER_API_ROUTE,
        headers = {
            'Authorization': f'Bearer {jwt}',
            'Content-Type': 'application/json'
        },
        data = dumps({
            'param': 'email',
            'current_val': 'jiro@email.com',
            'new_val': 'jiro@email.com'
        })
    )
    assert bad_resp1.status_code == 404
    assert bad_resp1.get_json()['msg'] == 'Current email incorrect'
   
    bad_resp2 = client.put(
        USER_API_ROUTE,
        headers = {
            'Authorization': f'Bearer {jwt}',
            'Content-Type': 'application/json'
        },
        data = dumps({
            'param': 'email',
            'current_val': user.email,
            'new_val': user.email
        })
    )
    assert bad_resp2.status_code == 409
    assert bad_resp2.get_json()['msg'] == 'New email already taken'
    
    good_resp1 = client.put(
        USER_API_ROUTE,
        headers = {
            'Authorization': f'Bearer {jwt}',
            'Content-Type': 'application/json'
        },
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
        headers = {
            'Authorization': f'Bearer {jwt}',
            'Content-Type': 'application/json'
        },
        data = dumps({
            'param': 'password',
            'current_val': 'Jiro123',
            'new_val': 'Jiro123'
        })
    )
    assert bad_resp3.status_code == 404
    assert bad_resp3.get_json()['msg'] == 'Current password incorrect'
    
    good_resp2 = client.put(
        USER_API_ROUTE,
        headers = {
            'Authorization': f'Bearer {jwt}',
            'Content-Type': 'application/json'
        },
        data = dumps({
            'param': 'password',
            'current_val': password,
            'new_val': 'Jiro123'
        })
    )
    assert good_resp2.status_code == 200
    assert good_resp2.get_json()['msg'] == 'Success'
    
    good_resp3 = client.put(
        USER_API_ROUTE,
        headers = {
            'Authorization': f'Bearer {jwt}',
            'Content-Type': 'application/json'
        },
        data = dumps({
            'param': 'name',
            'current_val': user.name,
            'new_val': 'Jiro'
        })
    )
    assert good_resp3.status_code == 200
    assert good_resp3.get_json()['msg'] == 'Success'

def test_user_delete(app: Flask) -> None:
    client = app.test_client()
    user, _ = sample_user(app)

    good_resp = client.delete(
        USER_API_ROUTE,
        headers = {'Authorization': f'Bearer {sample_jwt(app, user.id)}'}
    )
    assert good_resp.status_code == 200
    assert good_resp.get_json()['msg'] == 'Success'
