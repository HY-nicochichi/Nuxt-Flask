from typing import (
    Self,
    Literal
)
from pydantic import (
    BaseModel,
    field_validator,
    model_validator
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

    @field_validator('email', mode='after')
    @classmethod
    def email_validator(cls, val: str) -> str:
        return validate_email(val)

    @field_validator('password', mode='after')
    @classmethod
    def password_validator(cls, val: str) -> str:
        return validate_password(val)

    @field_validator('name', mode='after')
    @classmethod
    def name_validator(cls, val: str) -> str:
        return validate_name(val)

class UserPatch(BaseModel):
    param: Literal['email', 'password', 'name']
    current_val: str
    new_val: str

    @model_validator(mode='after')
    def user_patch_validator(self) -> Self:
        match self.param:
            case 'email':
                validate_email(self.current_val)
                validate_email(self.new_val)
            case 'password':
                validate_password(self.current_val)
                validate_password(self.new_val)
            case 'name':
                validate_name(self.current_val)
                validate_name(self.new_val)
        return self
