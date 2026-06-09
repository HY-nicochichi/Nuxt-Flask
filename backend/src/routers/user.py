from typing import Any
from flask import Blueprint, Response, jsonify
from flask_jwt_extended import jwt_required
from src.models import db_transaction
from src.models.user import User, current_user
from src.validations import validate_json
from src.validations.user import CreateUser, UpdateMe

bp_user = Blueprint('bp_user', __name__, url_prefix='/users')

@bp_user.post('')
@validate_json
def create_user(data: CreateUser) -> tuple[Response, int]:
    if User.find_by(email=data.email):
        return jsonify(msg='Email already taken'), 409
    with db_transaction():
        User.create(**data.model_dump())
    return Response(content_type='application/json'), 204

@bp_user.get('/me')
@jwt_required()
def get_me() -> tuple[Response, int]:
    return jsonify(email=current_user.email, name=current_user.name), 200

@bp_user.patch('/me')
@jwt_required()
@validate_json
def update_me(data: UpdateMe) -> tuple[Response, int]:
    new_values: dict[str, Any] = data.model_dump(
        exclude={'current_password'}, exclude_none=True
    )
    if not new_values:
        return jsonify(msg='No params to update'), 422
    if not current_user.check_password(data.current_password):
        return jsonify(msg='Invalid current password'), 422
    if data.email and User.find_by(email=data.email):
        return jsonify(msg='Email already taken'), 409
    with db_transaction():
        current_user.update(**new_values)
    return Response(content_type='application/json'), 204

@bp_user.delete('/me')
@jwt_required()
def delete_me() -> tuple[Response, int]:
    with db_transaction():
        current_user.delete()
    return Response(content_type='application/json'), 204
