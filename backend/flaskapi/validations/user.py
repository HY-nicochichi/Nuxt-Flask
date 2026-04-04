from typing import (
    Literal,
    Annotated
)
from pydantic import (
    BaseModel,
    AfterValidator,
    Field
)
from . import (
    validate_email,
    validate_password,
    validate_name
)

class UserPost(BaseModel):
    email: Annotated[str, AfterValidator(validate_email)]
    password: Annotated[str, AfterValidator(validate_password)]
    name: Annotated[str, AfterValidator(validate_name)]

class EmailPatch(BaseModel):
    param: Literal['email']
    current_val: Annotated[str, AfterValidator(validate_email)]
    new_val: Annotated[str, AfterValidator(validate_email)]

class PasswordPatch(BaseModel):
    param: Literal['password']
    current_val: Annotated[str, AfterValidator(validate_password)]
    new_val: Annotated[str, AfterValidator(validate_password)]

class NamePatch(BaseModel):
    param: Literal['name']
    current_val: Annotated[str, AfterValidator(validate_name)]
    new_val: Annotated[str, AfterValidator(validate_name)]

type UserPatch = Annotated[EmailPatch|PasswordPatch|NamePatch, Field(discriminator='param')]
