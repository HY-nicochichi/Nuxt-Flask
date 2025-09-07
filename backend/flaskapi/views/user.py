from flask import Blueprint
from flask_jwt_extended import (
    jwt_required,
    current_user
)
from models import User
from validations import validate_json
from validations.user import (
    UserPost,
    UserPut
)

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')

@bp_user.get('/')
@jwt_required()
def user_get() -> tuple[dict, int]:
    return {'email': current_user.email, 'name': current_user.name}, 200

@bp_user.post('/')
@validate_json
def user_post(data: UserPost) -> tuple[dict, int]:
    if User.create(data.email, data.password, data.name):
        return {'msg': 'Success'}, 200
    else:
        return {'msg': 'Email already taken'}, 409

@bp_user.put('/')
@jwt_required()
@validate_json
def user_put(data: UserPut) -> tuple[dict, int]:
    match data.param:
        case 'email':
            if current_user.email != data.current_val:
                return {'msg': 'Invalid current value'}, 400
            if User.search_by_email(data.new_val):
                return {'msg': 'New value already taken'}, 409
            current_user.update_email(data.new_val)
        case 'password':
            if not current_user.is_password_matched(data.current_val):
                return {'msg': 'Invalid current value'}, 400
            current_user.update_password(data.new_val)
        case 'name':
            if current_user.name != data.current_val:
                return {'msg': 'Invalid current value'}, 400
            current_user.update_name(data.new_val)
    return {'msg': 'Success'}, 200

@bp_user.delete('/')
@jwt_required()
def user_delete() -> tuple[dict, int]:
    current_user.delete()
    return {'msg': 'Success'}, 200
