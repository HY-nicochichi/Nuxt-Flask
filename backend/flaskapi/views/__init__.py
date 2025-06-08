from flask import (
    Blueprint,
    send_from_directory
)
from flask_swagger_ui import get_swaggerui_blueprint
from .jwt import bp_jwt
from .user import bp_user

bp_swagger: Blueprint = get_swaggerui_blueprint(
    base_url = '',
    api_url = '/swagger.yaml',
    blueprint_name = 'bp_swagger'
)

@bp_swagger.get('/swagger.yaml')
def swagger_yaml() -> tuple:
    return send_from_directory('/src', 'swagger.yaml'), 200

bps: list[Blueprint] = [
    bp_swagger,
    bp_jwt,
    bp_user
]
