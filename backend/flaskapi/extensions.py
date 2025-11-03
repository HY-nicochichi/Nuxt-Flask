from typing import Self
from uuid import uuid4
from contextlib import contextmanager
from datetime import (
    datetime,
    UTC
)
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

def uuid_str() -> str:
    return str(uuid4())

def utc_now() -> datetime:
    return datetime.now(UTC)

class Base(DeclarativeBase):
    __abstract__ = True
    id : Mapped[str] = mapped_column(default=uuid_str, primary_key=True)
    created: Mapped[datetime] = mapped_column(default=utc_now, nullable=False)
    updated: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now, nullable=False)

    @classmethod
    def search_by_id(cls, id: str) -> Self|None:
        return db_orm.session.scalars(select(cls).where(cls.id == id)).one_or_none()

    def delete(self) -> None:
        db_orm.session.delete(self)

db_orm = SQLAlchemy(model_class=Base)
jwt_manager = JWTManager()
cross_origin = CORS()

Model: type[Base] = db_orm.Model

@contextmanager
def db_transaction():
    try:
        yield
        db_orm.session.commit()
    except SQLAlchemyError:
        db_orm.session.rollback()
        raise
