from contextlib import contextmanager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

class Base(DeclarativeBase):
    __abstract__ = True
    id : Mapped[str] = mapped_column(primary_key=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now, nullable=False)

db_orm = SQLAlchemy(model_class=Base)
jwt_manager = JWTManager()
cross_origin = CORS()

@contextmanager
def db_transaction():
    try:
        yield
        db_orm.session.commit()
    except SQLAlchemyError as e:
        db_orm.session.rollback()
        raise e
