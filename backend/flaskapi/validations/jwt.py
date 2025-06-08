from typing import Annotated
from pydantic import (
    BaseModel,
    AfterValidator
)
from . import (
    validate_email,
    validate_password
)

class JWTPost(BaseModel):
    email: Annotated[str, AfterValidator(validate_email)]
    password: Annotated[str, AfterValidator(validate_password)]
