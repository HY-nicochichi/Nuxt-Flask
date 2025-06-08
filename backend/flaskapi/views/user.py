from flask import Blueprint
from flask_jwt_extended import jwt_required
from models import (
    User,
    current_user
)
from validations import validate_json
from validations.user import (
    UserPost,
    UserPatch
)
from extensions import db_transaction

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')

@bp_user.get('/')
@jwt_required()
def user_get() -> tuple:
    return {'email': current_user.email, 'name': current_user.name}, 200

@bp_user.post('/')
@validate_json
def user_post(data: UserPost) -> tuple:
    with db_transaction():
        user = User.create(data.email, data.password, data.name) 
    if user:
        return {'id': user.id}, 201
    else:
        return {'msg': 'Email already taken'}, 409

@bp_user.patch('/')
@jwt_required()
@validate_json
def user_patch(data: UserPatch) -> tuple:
    match data.param:
        case 'email':
            if current_user.email != data.current_val:
                return {'msg': 'Invalid current value'}, 400
            elif User.find_by_email(data.new_val):
                return {'msg': 'New value already taken'}, 409
        case 'password':
            if not current_user.is_password_matched(data.current_val):
                return {'msg': 'Invalid current value'}, 400
        case 'name':
            if current_user.name != data.current_val:
                return {'msg': 'Invalid current value'}, 400
    with db_transaction():
        match data.param:
            case 'email':
                current_user.email = data.new_val
            case 'password':
                current_user.update_password(data.new_val)
            case 'name':
                current_user.name = data.new_val
    return '', 204

@bp_user.delete('/')
@jwt_required()
def user_delete() -> tuple:
    with db_transaction():
        current_user.delete()
    return '', 204
