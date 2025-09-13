from typing import Type
from functools import wraps
from re import fullmatch
from pydantic import (
    BaseModel,
    ValidationError
)
from flask import request

def validate_json(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            DataModel: Type[BaseModel] = func.__annotations__['data']
            data = DataModel.model_validate(request.get_json(silent=True))
            return func(data, *args, **kwargs)
        except (TypeError, ValidationError):
            return {'msg': 'Invalid Content-Type header or JSON body'}, 400
    return wrapped

def validate_email(val: str) -> str:
    if not fullmatch(r'^(?=.{10,32}$)[a-z0-9.-]+@[a-z0-9-]+\.[a-z0-9.-]+$', val):
        raise ValueError
    return val

def validate_password(val: str) -> str:
    if not fullmatch(r'(?=.{8,16})(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]+', val):
        raise ValueError
    return val

def validate_name(val: str) -> str:
    if not fullmatch(r'.{1,16}', val):
        raise ValueError
    return val
