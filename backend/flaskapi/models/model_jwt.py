from pydantic import (
    BaseModel,
    Field
)

class JWTPost(BaseModel):
    email: str = Field(min_length=3)
    password: str = Field(min_length=6, max_length=20)
