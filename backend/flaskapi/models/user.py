from typing import Self
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from extensions import db_orm

class User(db_orm.Model):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    @classmethod
    def search_by_id(cls: Self, id: str) -> Self|None:
        return db_orm.session.scalars(select(cls).where(cls.id == id)).one_or_none()

    @classmethod
    def search_by_email(cls: Self, email: str) -> Self|None:
        return db_orm.session.scalars(select(cls).where(cls.email == email)).one_or_none()

    @classmethod
    def create(cls: Self, email: str, password: str, name: str) -> Self|None:
        if cls.search_by_email(email):
            return None
        else:
            user = cls(
                id = str(uuid4()),
                email = email,
                password_hash = generate_password_hash(password),
                name = name
            )
            db_orm.session.add(user)
            db_orm.session.commit()
            return user

    def is_password_matched(self: Self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def update_email(self: Self, email: str) -> None:
        self.email = email
        db_orm.session.commit()

    def update_password(self: Self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
        db_orm.session.commit()
    
    def update_name(self: Self, name: str) -> None:
        self.name = name
        db_orm.session.commit()

    def delete(self: Self) -> None:
        db_orm.session.delete(self)
        db_orm.session.commit()
