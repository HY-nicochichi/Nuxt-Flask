from pydantic import ValidationError
from flask import (
    Blueprint,
    request
)
from flask_jwt_extended import create_access_token
from helpers import user_helper
from models import JWTPost

bp_jwt = Blueprint('bp_jwt', __name__, url_prefix='/jwt')

@bp_jwt.post('/')
def jwt_post() -> tuple[dict, int]:
    try:
        data = JWTPost.model_validate(request.get_json(silent=True))
    except (TypeError, ValidationError):
        return {'msg': 'Invalid Content-Type header or JSON body'}, 400
    msg, id = user_helper.authenticate(data)
    if msg == 'Success':
        access_token: str = create_access_token(identity=id)
        return {'msg': msg, 'access_token': access_token}, 200
    else:
        return {'msg': msg}, 401
