from typing import Self, Any, cast
from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import datetime, UTC
from uuid import UUID, uuid7
from sqlalchemy import (
    ColumnElement, Select,
    select, insert, update, delete, inspect
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from src.extensions import orm

@contextmanager
def db_transaction() -> Generator[None, None, None]:
    try:
        yield
        orm.session.commit()
    except Exception:
        orm.session.rollback()
        raise

def utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)

type QueryFunc = Callable[[Select[tuple]], Select[tuple]]

class AppModel(DeclarativeBase):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(default=uuid7, primary_key=True)
    created: Mapped[datetime] = mapped_column(default=utc_now)
    updated: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    @classmethod
    def all(cls, *args: QueryFunc) -> list[Self]:
        statement: Select[tuple[Self]] = select(cls)
        for arg in args:
            statement = arg(statement)
        return cast(list[Self], orm.session.scalars(statement).unique().all())

    @classmethod
    def calc[T](cls, element: ColumnElement[T], *args: QueryFunc) -> T|None:
        statement: Select[tuple[T]] = select(element).select_from(cls)
        for arg in args:
            statement = arg(statement)
        return orm.session.scalar(statement)

    @classmethod
    def bulk_create(cls, data_list: list[dict[str, Any]]) -> list[UUID]:
        now: datetime = utc_now()
        _data_list: list[dict[str, Any]] = [
            {'id': uuid7(), 'created': now, 'updated': now, **data}
            for data in data_list
        ]
        orm.session.execute(insert(cls), _data_list)
        return [data['id'] for data in _data_list]

    @classmethod
    def bulk_update(cls, data_list: list[dict[str, Any]]) -> None:
        now: datetime = utc_now()
        _data_list: list[dict[str, Any]] = [
            {'updated': now, **data} for data in data_list
        ]
        orm.session.execute(update(cls), _data_list)

    @classmethod
    def bulk_delete(cls, id_list: list[UUID]) -> None:
        orm.session.execute(delete(cls).where(cls.id.in_(id_list)))

    @classmethod
    def find_by(cls, **kwargs) -> Self|None:
        return orm.session.scalars(select(cls).filter_by(**kwargs)).one_or_none()

    @classmethod
    def create(cls, **kwargs) -> Self:
        instance: Self = cls(**kwargs)
        orm.session.add(instance)
        orm.session.flush()
        return instance

    def update(self, **kwargs) -> None:
        for key, val in kwargs.items():
            setattr(self, key, val)
        orm.session.flush()

    def delete(self) -> None:
        orm.session.delete(self)
        orm.session.flush()

    def to_dict(
        self, include: set[str]|None = None, exclude: set[str]|None = None
    ) -> dict[str, Any]:
        keys: set[str] = set(inspect(self).mapper.column_attrs.keys())
        if include:
            keys &= include
        if exclude:
            keys -= exclude
        return {key: getattr(self, key) for key in keys}

class Q:
    @staticmethod
    def where(*args, **kwargs) -> QueryFunc:
        def _where(statement: Select[tuple]) -> Select[tuple]:
            if args:
                statement = statement.where(*args)
            if kwargs:
                statement = statement.filter_by(**kwargs)
            return statement
        return _where

    @staticmethod
    def offset_limit(offset: int|None = None, limit: int|None = None) -> QueryFunc:
        def _offset_limit(statement: Select[tuple]) -> Select[tuple]:
            if offset:
                statement = statement.offset(offset)
            if limit:
                statement = statement.limit(limit)
            return statement
        return _offset_limit

    @staticmethod
    def order_by(*args) -> QueryFunc:
        def _order_by(statement: Select[tuple]) -> Select[tuple]:
            return statement.order_by(*args)
        return _order_by

    @staticmethod
    def group_by(*args) -> QueryFunc:
        def _group_by(statement: Select[tuple]) -> Select[tuple]:
            return statement.group_by(*args)
        return _group_by

    @staticmethod
    def having(*args) -> QueryFunc:
        def _having(statement: Select[tuple]) -> Select[tuple]:
            return statement.having(*args)
        return _having

    @staticmethod
    def join(*args, **kwargs) -> QueryFunc:
        def _join(statement: Select[tuple]) -> Select[tuple]:
            return statement.join(*args, **kwargs)
        return _join

    @staticmethod
    def options(*args) -> QueryFunc:
        def _options(statement: Select[tuple]) -> Select[tuple]:
            return statement.options(*args)
        return _options
