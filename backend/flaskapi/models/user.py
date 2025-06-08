from typing import Self
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from extensions import AppModel

class User(AppModel):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    @classmethod
    def create(cls, **kwargs) -> Self|None:
        if not cls.find_by(email=kwargs.get('email')):
            kwargs['password_hash'] = generate_password_hash(kwargs.pop('password'))
            return super().create(**kwargs)

    def is_password_matched(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def update(self, **kwargs) -> None:
        if 'password' in kwargs:
            kwargs['password_hash'] = generate_password_hash(kwargs.pop('password'))
        super().update(**kwargs)
