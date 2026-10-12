from typing import Annotated
from pydantic import BaseModel, AfterValidator
from src.validations import (
    lower_str, validate_email, validate_password, validate_name
)

class CreateUser(BaseModel):
    email: Annotated[str, AfterValidator(lower_str(validate_email))]
    password: Annotated[str, AfterValidator(validate_password)]
    name: Annotated[str, AfterValidator(validate_name)]

class UpdateMe(BaseModel):
    current_password: Annotated[str, AfterValidator(validate_password)]
    email: Annotated[str|None, AfterValidator(lower_str(validate_email))] = None
    password: Annotated[str|None, AfterValidator(validate_password)] = None
    name: Annotated[str|None, AfterValidator(validate_name)] = None
