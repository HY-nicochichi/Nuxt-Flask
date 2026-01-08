from extensions import jwt_manager
from .user import User

@jwt_manager.user_lookup_loader
def lookup_user(header: dict, data: dict) -> User|None:
    return User.search_by_id(data['sub'])
