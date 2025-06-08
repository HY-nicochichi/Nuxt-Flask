from uuid import uuid4
from typing import Self
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_jwt_extended import current_user
from models import (
    JWTPost,
    User,
    UserPost,
    UserPut
)
from extensions import db_orm

class UserHelper():

    def search_by_id(self: Self, id: str) -> User|None:
        return User.query.filter_by(id=id).one_or_none()
    
    def search_by_email(self: Self, email: str) -> User|None:
        return User.query.filter_by(email=email).one_or_none()

    def authenticate(self: Self, data: JWTPost) -> dict[str, str]:
        user: User|None = self.search_by_email(data.email)
        if user == None:
            return {'msg': 'Email incorrect'}
        elif check_password_hash(user.password_hash, data.password) == False:
            return {'msg': 'Password incorrect'}
        else:
            return {'msg': 'Success', 'id': user.id}

    def create(self: Self, data: UserPost) -> tuple[str, int]:
        if self.search_by_email(data.email):
            return 'Email already taken', 409
        else: 
            password_hash: str = generate_password_hash(data.password)
            new_user = User(
                id=str(uuid4()),
                email=data.email,
                password_hash=password_hash,
                name=data.name
            )
            db_orm.session.add(new_user)
            db_orm.session.commit()
            return 'Success', 200

    def update_email(self: Self, data: UserPut) -> tuple[str, int]:
        if current_user.email != data.current_val:
            return 'Current email incorrect', 404
        elif self.search_by_email(data.new_val) != None:
            return 'New email already taken', 409
        else:
            current_user.email = data.new_val
            db_orm.session.commit()
            return 'Success', 200
    
    def update_password(self: Self, data: UserPut) -> tuple[str, int]:
        if check_password_hash(current_user.password_hash, data.current_val) == False:
            return 'Current password incorrect', 404
        else:
            current_user.password_hash = generate_password_hash(data.new_val)
            db_orm.session.commit()
            return 'Success', 200

    def update_name(self: Self, data: UserPut) -> tuple[str, int]:
        if current_user.name != data.current_val:
            return 'Current name incorrect', 404
        else:
            current_user.name = data.new_val
            db_orm.session.commit()
            return 'Success', 200

    def delete(self: Self) -> None:
        db_orm.session.delete(current_user)
        db_orm.session.commit()
