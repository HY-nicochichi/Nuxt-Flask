from typing import Annotated
from pydantic import BaseModel, AfterValidator
from src.validations import validate_email, validate_password

class CreateToken(BaseModel):
    email: Annotated[str, AfterValidator(validate_email)]
    password: Annotated[str, AfterValidator(validate_password)]
