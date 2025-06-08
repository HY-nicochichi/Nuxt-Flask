from flask import (
    Blueprint,
    Response,
    jsonify
)
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
def user_get() -> tuple[Response, int]:
    return jsonify(email=current_user.email, name=current_user.name), 200

@bp_user.post('/')
@validate_json
def user_post(data: UserPost) -> tuple[Response, int]:
    with db_transaction():
        user = User.create(**data.model_dump())
    if user:
        return Response(content_type='application/json'), 204
    else:
        return jsonify(msg='Email already taken'), 409

@bp_user.patch('/')
@jwt_required()
@validate_json
def user_patch(data: UserPatch) -> tuple[Response, int]:
    match data.param:
        case 'email':
            if current_user.email != data.current_val:
                return jsonify(msg='Invalid current value'), 422
            elif User.find_by(email=data.new_val):
                return jsonify(msg='New value already taken'), 409
        case 'password':
            if not current_user.is_password_matched(data.current_val):
                return jsonify(msg='Invalid current value'), 422
        case 'name':
            if current_user.name != data.current_val:
                return jsonify(msg='Invalid current value'), 422
    with db_transaction():
        current_user.update(**{data.param: data.new_val})
    return Response(content_type='application/json'), 204

@bp_user.delete('/')
@jwt_required()
def user_delete() -> tuple[Response, int]:
    with db_transaction():
        current_user.delete()
    return Response(content_type='application/json'), 204
