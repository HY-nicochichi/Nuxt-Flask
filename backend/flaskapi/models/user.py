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
    AppModel
)

class User(AppModel):
    __tablename__ = 'users'
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    @classmethod
    def find_by_email(cls, email: str) -> Self|None:
        return db_orm.session.scalars(select(cls).where(cls.email == email)).one_or_none()

    @classmethod
    def create(cls, email: str, password: str, name: str) -> Self|None:
        if not cls.find_by_email(email):
            return super().create(
                email = email,
                password_hash = generate_password_hash(password),
                name = name
            )

    def is_password_matched(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def update_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
