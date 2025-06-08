from typing import (
    Self,
    Literal,
    Annotated
)
from pydantic import (
    BaseModel,
    AfterValidator,
    model_validator
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
