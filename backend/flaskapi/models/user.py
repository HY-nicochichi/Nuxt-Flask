from typing import Self
from sqlalchemy import select
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from extensions import (
    db_orm,
    Model
)

class User(Model):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    @classmethod
    def search_by_email(cls, email: str) -> Self|None:
        return db_orm.session.scalars(select(cls).where(cls.email == email)).one_or_none()

    @classmethod
    def create(cls, email: str, password: str, name: str) -> Self|None:
        if cls.search_by_email(email):
            return None
        else:
            user = cls(
                email = email,
                password_hash = generate_password_hash(password),
                name = name
            )
            db_orm.session.add(user)
            return user

    def is_password_matched(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def update_email(self, email: str) -> None:
        self.email = email

    def update_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
    
    def update_name(self, name: str) -> None:
        self.name = name
