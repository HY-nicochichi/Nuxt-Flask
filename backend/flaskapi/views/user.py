from flask import Blueprint
from flask_jwt_extended import (
    jwt_required,
    get_current_user
)
from models import User
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
    user: User = get_current_user()
    return {'email': user.email, 'name': user.name}, 200

@bp_user.post('/')
@validate_json
def user_post(data: UserPost) -> tuple:
    with db_transaction():
        user = User.create(data.email, data.password, data.name) 
    if not user:
        return {'msg': 'Email already taken'}, 409
    return {'msg': 'Success'}, 201

@bp_user.patch('/')
@jwt_required()
@validate_json
def user_patch(data: UserPatch) -> tuple:
    user: User = get_current_user()
    match data.param:
        case 'email':
            if user.email != data.current_val:
                return {'msg': 'Invalid current value'}, 400
            elif User.search_by_email(data.new_val):
                return {'msg': 'New value already taken'}, 409
        case 'password':
            if not user.is_password_matched(data.current_val):
                return {'msg': 'Invalid current value'}, 400
        case 'name':
            if user.name != data.current_val:
                return {'msg': 'Invalid current value'}, 400
    with db_transaction():
        match data.param:
            case 'email':
                user.update_email(data.new_val)
            case 'password':
                user.update_password(data.new_val)
            case 'name':
                user.update_name(data.new_val)
    return {'msg': 'Success'}, 200

@bp_user.delete('/')
@jwt_required()
def user_delete() -> tuple:
    user: User = get_current_user()
    with db_transaction():
        user.delete()
    return '', 204
