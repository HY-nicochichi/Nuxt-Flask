from pydantic import (
    BaseModel,
    Field
)

class JWTPost(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
