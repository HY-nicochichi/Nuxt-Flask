from typing import Literal
from pydantic import (
    BaseModel,
    Field
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from extensions import db_orm

class User(db_orm.Model):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

class UserPost(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=6, max_length=20)
    name: str = Field(min_length=1)

class UserPut(BaseModel):
    param: Literal['email', 'password', 'name']
    current_val: str = Field(min_length=1)
    new_val: str = Field(min_length=1)
