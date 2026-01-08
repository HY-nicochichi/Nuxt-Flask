from pydantic import (
    BaseModel,
    field_validator
)
from . import (
    validate_email,
    validate_password
)

class JWTPost(BaseModel):
    email: str
    password: str

    @field_validator('email', mode='after')
    @classmethod
    def email_validator(cls, val: str) -> str:
        return validate_email(val)

    @field_validator('password', mode='after')
    @classmethod
    def password_validator(cls, val: str) -> str:
        return validate_password(val)
