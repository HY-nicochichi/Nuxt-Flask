from flask import Blueprint, Response, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from src.routers.token import bp_token
from src.routers.user import bp_user

bp_swagger: Blueprint = get_swaggerui_blueprint(
    base_url = '', api_url = '/swagger.yaml', blueprint_name = 'bp_swagger'
)

@bp_swagger.get('/swagger.yaml')
def swagger_yaml() -> tuple[Response, int]:
    return send_from_directory('/app', 'swagger.yaml'), 200

blueprints: list[Blueprint] = [bp_swagger, bp_token, bp_user]
