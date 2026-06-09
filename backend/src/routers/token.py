from flask import Blueprint, Response, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token
)
from src.models.user import User, current_user
from src.validations import validate_json
from src.validations.token import CreateToken

bp_token = Blueprint('bp_token', __name__, url_prefix='/tokens')

@bp_token.post('')
@validate_json
def create_token(data: CreateToken) -> tuple[Response, int]:
    user: User|None = User.find_by(email=data.email)
    if user and user.check_password(data.password):
        return jsonify(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id))
        ), 200
    else:
        return jsonify(msg='Invalid email or password'), 401

@bp_token.post('/refresh')
@jwt_required(refresh=True)
def refresh_token() -> tuple[Response, int]:
    return jsonify(access_token=create_access_token(str(current_user.id))), 200
