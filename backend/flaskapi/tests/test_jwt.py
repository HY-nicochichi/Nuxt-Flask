from json import dumps
from flask import Flask
from flask_jwt_extended import decode_token
from . import (
    app,
    sample_user
)

JWT_API_ROUTE = '/jwt/'

def test_jwt_post(app: Flask) -> None:
    client = app.test_client()
    user, password = sample_user(app)
    
    bad_resp1 = client.post(
        JWT_API_ROUTE,
        data = dumps({
            'email': user.email,
            'password': password
        })
    )
    assert bad_resp1.status_code == 400
    assert bad_resp1.get_json()['msg'] == 'Invalid Content-Type header or JSON body'
    
    bad_resp2 = client.post(
        JWT_API_ROUTE,
        headers = {'Content-Type': 'application/json'},
        data = dumps({
            'email': None,
            'password': password
        })
    )
    assert bad_resp2.status_code == 400
    assert bad_resp2.get_json()['msg'] == 'Invalid Content-Type header or JSON body'
    
    bad_resp3 = client.post(
        JWT_API_ROUTE,
        headers = {'Content-Type': 'application/json'},
        data = dumps({
           'email': 'jiro@email.com',
           'password': password
        })
    )
    assert bad_resp3.status_code == 401
    assert bad_resp3.get_json()['msg'] == 'Email incorrect'
    
    bad_resp4 = client.post(
        JWT_API_ROUTE,
        headers = {'Content-Type': 'application/json'},
        data = dumps({
            'email': user.email,
            'password': 'Jiro1234'
        })
    )
    assert bad_resp4.status_code == 401
    assert bad_resp4.get_json()['msg'] == 'Password incorrect'
    
    good_resp = client.post(
        JWT_API_ROUTE,
        headers = {'Content-Type': 'application/json'},
        data = dumps({
            'email': user.email,
            'password': password
        })
    )
    assert good_resp.status_code == 200
    assert good_resp.get_json()['msg'] == 'Success'
    with app.app_context():
        access_token = good_resp.get_json()['access_token']
        assert decode_token(access_token)['sub'] == user.id
