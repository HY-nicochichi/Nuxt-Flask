from typing import (
    Self,
    Literal
)
from pydantic import (
    BaseModel,
    ValidationInfo,
    field_validator
)
from . import (
    validate_email,
    validate_password,
    validate_name
)

class UserPost(BaseModel):
    email: str
    password: str
    name: str

    @field_validator('email')
    def email_validator(cls: Self, val: str) -> str:
        return validate_email(val)
    
    @field_validator('password')
    def password_validator(cls: Self, val: str) -> str:
        return validate_password(val)

class UserPut(BaseModel):
    param: Literal['email', 'password', 'name']
    current_val: str
    new_val: str

    @field_validator('current_val')
    def current_val_validator(cls: Self, val: str, info: ValidationInfo) -> str:
        match info.data.get('param'):
            case 'email':
                return validate_email(val)
            case 'password':
                return validate_password(val)
            case 'name':
                return validate_name(val)
    
    @field_validator('new_val')
    def new_val_validator(cls: Self, val: str, info: ValidationInfo) -> str:
        match info.data.get('param'):
            case 'email':
                return validate_email(val)
            case 'password':
                return validate_password(val)
            case 'name':
                return validate_name(val)
