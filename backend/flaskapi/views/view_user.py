from pydantic import ValidationError
from flask import (
    Blueprint,
    request
)
from flask_jwt_extended import (
    jwt_required,
    current_user
)
from helpers import user_helper
from models import (
    UserPost,
    UserPut
)

bp_user = Blueprint('bp_user', __name__, url_prefix='/user')

@bp_user.get('/')
@jwt_required()
def user_get() -> tuple[dict, int]:
    return {'email': current_user.email, 'name': current_user.name}, 200

@bp_user.post('/')
def user_post() -> tuple[dict, int]:
    try:
        data = UserPost.model_validate(request.get_json(silent=True))
    except (TypeError, ValidationError):
        return {'msg': 'Invalid Content-Type header or JSON body'}, 400
    msg, status = user_helper.create(data)
    return {'msg': msg}, status

@bp_user.put('/')
@jwt_required()
def user_put() -> tuple[dict, int]:
    try:
        data = UserPut.model_validate(request.get_json(silent=True))
    except (TypeError, ValidationError):
        return {'msg': 'Invalid Content-Type header or JSON body'}, 400
    match data.param:
        case 'email':
            msg, status = user_helper.update_email(data)
        case 'password':
            msg, status = user_helper.update_password(data)
        case 'name':
            msg, status = user_helper.update_name(data)    
    return {'msg': msg}, status

@bp_user.delete('/')
@jwt_required()
def user_delete() -> tuple[dict, int]:
    user_helper.delete()
    return {'msg': 'Success'}, 200
