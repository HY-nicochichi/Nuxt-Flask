from typing import Self
from collections.abc import Callable
from contextlib import contextmanager
from uuid import (
    UUID,
    uuid7
)
from datetime import (
    datetime,
    UTC
)
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import (
    Select,
    select
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)

class Base(DeclarativeBase):
    __abstract__ = True
    id : Mapped[UUID] = mapped_column(default=uuid7, primary_key=True)
    created: Mapped[datetime] = mapped_column(default=utc_now, nullable=False)
    updated: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now, nullable=False)

db_orm = SQLAlchemy(model_class=Base)
jwt_manager = JWTManager()
cross_origin = CORS()

@contextmanager
def db_transaction():
    try:
        yield
        db_orm.session.commit()
    except Exception:
        db_orm.session.rollback()
        raise

class AppModel(Base):
    __abstract__ = True

    @classmethod
    def all(cls, *args: Callable[[Select], Select]) -> list[Self]:
        statement: Select = select(cls)
        for arg in args:
            statement = arg(statement)
        return db_orm.session.scalars(statement).all()

    @classmethod
    def find_by(cls, **kwargs) -> Self|None:
        return db_orm.session.scalars(select(cls).filter_by(**kwargs)).one_or_none()

    @classmethod
    def create(cls, **kwargs) -> Self:
        instance = cls(**kwargs)
        db_orm.session.add(instance)
        db_orm.session.flush()
        return instance

    def update(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)
        db_orm.session.flush()

    def delete(self) -> None:
        db_orm.session.delete(self)
        db_orm.session.flush()

    def to_dict(self) -> dict:
        dictionary: dict = self.__dict__.copy()
        dictionary.pop('_sa_instance_state')
        return dictionary
