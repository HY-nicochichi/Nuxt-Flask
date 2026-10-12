from typing import Annotated
from pydantic import BaseModel, AfterValidator
from src.validations import lower_str, validate_email, validate_password

class CreateToken(BaseModel):
    email: Annotated[str, AfterValidator(lower_str(validate_email))]
    password: Annotated[str, AfterValidator(validate_password)]
