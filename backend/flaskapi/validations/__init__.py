from typing import Type
from functools import wraps
from re import fullmatch
from pydantic import (
    BaseModel,
    ValidationError
)
from pydantic_core import PydanticCustomError
from flask import request
from werkzeug.exceptions import (
    BadRequest,
    UnsupportedMediaType
)

def validate_json(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            DataModel: Type[BaseModel] = func.__annotations__['data']
            data = DataModel.model_validate(request.get_json())
            return func(data, *args, **kwargs)
        except UnsupportedMediaType:
            return {'msg': 'Invalid Content-Type header'}, 415
        except BadRequest:
            return {'msg': 'Invalid JSON body syntax'}, 400
        except ValidationError as e:
            return {'validation_error': e.errors()}, 422
    return wrapped

def validate_email(val: str) -> str:
    if not fullmatch(r'^(?=.{10,32}$)[a-z0-9.-]+@[a-z0-9-]+\.[a-z0-9.-]+$', val):
        raise PydanticCustomError(
            'value_error',
            'Email must be 10-32 characters and a standard email format'
        )
    return val

def validate_password(val: str) -> str:
    if not fullmatch(r'(?=.{8,16})(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]+', val):
        raise PydanticCustomError(
            'value_error',
            'Password must be 8-16 characters and include at least 1 uppercase, 1 lowercase, and 1 number'
        )
    return val

def validate_name(val: str) -> str:
    if not fullmatch(r'.{1,16}', val):
        raise PydanticCustomError(
            'value_error',
            'Name must be 1-16 characters'
        )
    return val
