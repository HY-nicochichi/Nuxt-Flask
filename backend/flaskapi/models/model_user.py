from typing import (
    Self,
    Literal
)
from pydantic import (
    BaseModel,
    ValidationInfo,
    field_validator
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from extensions import db_orm
from .validate_func import (
    validate_email,
    validate_password,
    validate_name
)

class User(db_orm.Model):
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

class UserPost(BaseModel):
    email: str
    password: str
    name: str

    @field_validator('email')
    def email_validator(cls: Self, val: str) -> str:
        validate_email(val)
        return val
    
    @field_validator('password')
    def password_validator(cls: Self, val: str) -> str:
        validate_password(val)
        return val

class UserPut(BaseModel):
    param: Literal['email', 'password', 'name']
    current_val: str
    new_val: str

    @field_validator('current_val')
    def current_val_validator(cls: Self, val: str, info: ValidationInfo) -> str:
        match info.data.get('param'):
            case 'email':
                validate_email(val)
            case 'password':
                validate_password(val)
            case 'name':
                validate_name(val)
        return val
    
    @field_validator('new_val')
    def new_val_validator(cls: Self, val: str, info: ValidationInfo) -> str:
        match info.data.get('param'):
            case 'email':
                validate_email(val)
            case 'password':
                validate_password(val)
            case 'name':
                validate_name(val)
        return val
