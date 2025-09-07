from flask import (
    Blueprint,
    send_from_directory
)
from flask_swagger_ui import get_swaggerui_blueprint
from .jwt import bp_jwt
from .user import bp_user

bp_swagger = get_swaggerui_blueprint(
    base_url = '',
    api_url = 'http://localhost:5000/swagger.json',
    blueprint_name = 'bp_swagger'
)

@bp_swagger.get('/swagger.json')
def swagger_json():
    return send_from_directory('/', 'swagger.json')

bps: list[Blueprint] = [
    bp_swagger,
    bp_jwt,
    bp_user
]
