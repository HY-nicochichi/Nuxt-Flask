from flask import Blueprint
from flask_jwt_extended import create_access_token
from models import User
from validations import validate_json
from validations.jwt import JWTPost

bp_jwt = Blueprint('bp_jwt', __name__, url_prefix='/jwt')

@bp_jwt.post('/')
@validate_json
def jwt_post(data: JWTPost) -> tuple:
    user: User|None = User.find_by_email(data.email)
    if user and user.is_password_matched(data.password):
        return {'access_token': create_access_token(user.id)}, 200
    else:
        return {'msg': 'Invalid email or password'}, 401
