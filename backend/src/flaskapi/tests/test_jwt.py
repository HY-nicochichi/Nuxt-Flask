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

JWT_API_ROUTE = '/jwt/'

def test_jwt_post(
    app: Flask, client: FlaskClient, password: str, user: User, headers: dict[str, str]
) -> None:
    bad_resp1 = client.post(
        JWT_API_ROUTE,
        data = dumps({
            'email': user.email,
            'password': password
        })
    )
    assert bad_resp1.status_code == 415
    assert bad_resp1.get_json()['msg'] == 'Invalid Content-Type header'

    bad_resp2 = client.post(
        JWT_API_ROUTE,
        headers = headers,
        data = 'invalid'
    )
    assert bad_resp2.status_code == 400
    assert bad_resp2.get_json()['msg'] == 'Invalid JSON body syntax'
    
    bad_resp3 = client.post(
        JWT_API_ROUTE,
        headers = headers,
        data = dumps({
            'email': user.email,
            'password': 'invalid'
        })
    )
    assert bad_resp3.status_code == 422
    assert bad_resp3.get_json()['validation_error'][0]['loc'] == ['password']
    
    bad_resp4 = client.post(
        JWT_API_ROUTE,
        headers = headers,
        data = dumps({
            'email': 'jiro@email.com',
            'password': password
        })
    )
    assert bad_resp4.status_code == 401
    assert bad_resp4.get_json()['msg'] == 'Invalid email or password'
    
    bad_resp5 = client.post(
        JWT_API_ROUTE,
        headers = headers,
        data = dumps({
            'email': user.email,
            'password': 'Jiro1234'
        })
    )
    assert bad_resp5.status_code == 401
    assert bad_resp5.get_json()['msg'] == 'Invalid email or password'
    
    good_resp = client.post(
        JWT_API_ROUTE,
        headers = headers,
        data = dumps({
            'email': user.email,
            'password': password
        })
    )
    assert good_resp.status_code == 200
    with app.app_context():
        access_token = good_resp.get_json()['access_token']
        assert decode_token(access_token)['sub'] == user.id
