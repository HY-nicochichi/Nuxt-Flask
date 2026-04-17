from typing import Annotated
from pydantic import (
    BaseModel,
    AfterValidator
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

class UserPatch(BaseModel):
    current_password: Annotated[str, AfterValidator(validate_password)]
    email: Annotated[str|None, AfterValidator(validate_email)] = None
    password: Annotated[str|None, AfterValidator(validate_password)] = None
    name: Annotated[str|None, AfterValidator(validate_name)] = None
