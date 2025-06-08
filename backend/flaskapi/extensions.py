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

db_orm = SQLAlchemy(model_class=Base)
jwt_manager = JWTManager()
cross_origin = CORS()

@contextmanager
def db_transaction():
    try:
        yield
        db_orm.session.commit()
    except Exception as e:
        db_orm.session.rollback()
        print(f'[{utc_now()}] ERROR in db_transaction: {e!r}')
        raise

class AppModel(Base):
    __abstract__ = True

    @classmethod
    def all(cls) -> list[Self]:
        return list(db_orm.session.scalars(select(cls)).all())

    @classmethod
    def where(cls, *args) -> list[Self]:
        return list(db_orm.session.scalars(select(cls).where(*args)).all())

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
