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

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')

@bp_user.get('/')
@jwt_required()
def user_get() -> tuple[dict, int]:
    user: User = get_current_user()
    return {'email': user.email, 'name': user.name}, 200

@bp_user.post('/')
@validate_json
def user_post(data: UserPost) -> tuple[dict, int]:
    if User.create(data.email, data.password, data.name):
        return {'msg': 'Success'}, 201
    else:
        return {'msg': 'Email already taken'}, 409

@bp_user.patch('/')
@jwt_required()
@validate_json
def user_patch(data: UserPatch) -> tuple[dict, int]:
    user: User = get_current_user()
    match data.param:
        case 'email':
            if user.email != data.current_val:
                return {'msg': 'Invalid current value'}, 400
            elif User.search_by_email(data.new_val):
                return {'msg': 'New value already taken'}, 409
            else:
                user.update_email(data.new_val)
        case 'password':
            if not user.is_password_matched(data.current_val):
                return {'msg': 'Invalid current value'}, 400
            else:
                user.update_password(data.new_val)
        case 'name':
            if user.name != data.current_val:
                return {'msg': 'Invalid current value'}, 400
            else:
                user.update_name(data.new_val)
    return {'msg': 'Success'}, 200

@bp_user.delete('/')
@jwt_required()
def user_delete() -> tuple[str, int]:
    user: User = get_current_user()
    user.delete()
    return '', 204
