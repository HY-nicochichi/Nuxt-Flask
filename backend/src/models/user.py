from typing import Self, Any, cast
from uuid import UUID
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.local import LocalProxy
from flask_jwt_extended import get_current_user
from src.extensions import jwt
from src.models import AppModel

pwd_hasher = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1)

class User(AppModel):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(30))

    @staticmethod
    def with_hashed_password(data: dict[str, Any]) -> dict[str, Any]:
        _data: dict[str, Any] = data.copy()
        if 'password' in _data:
            _data['password_hash'] = pwd_hasher.hash(_data.pop('password'))
        return _data

    @classmethod
    def create(cls, **kwargs) -> Self:
        return super().create(**cls.with_hashed_password(kwargs))

    def update(self, **kwargs) -> None:
        super().update(**self.with_hashed_password(kwargs))

    def check_password(self, password: str) -> bool:
        try:
            return pwd_hasher.verify(self.password_hash, password)
        except VerifyMismatchError:
            return False

@jwt.user_lookup_loader
def lookup_user(header: dict, data: dict) -> User|None:
    return User.find_by(id=UUID(data['sub']))

current_user = cast(User, LocalProxy(get_current_user))
