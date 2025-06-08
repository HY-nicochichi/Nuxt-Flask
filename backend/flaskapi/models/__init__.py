from werkzeug.local import LocalProxy
from flask_jwt_extended import get_current_user
from extensions import jwt_manager
from .user import User

@jwt_manager.user_lookup_loader
def lookup_user(header: dict, data: dict) -> User|None:
    return User.find_by_id(data['sub'])

current_user: User = LocalProxy(get_current_user)
