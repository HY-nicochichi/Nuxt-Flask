from functools import wraps
from re import search
from inspect import signature
from pydantic import (
    BaseModel,
    ValidationError
)
from flask import request

def validate_json(func):
    schema_type: BaseModel = signature(func).parameters['data'].annotation
    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            data = schema_type.model_validate(request.get_json(silent=True))
            return func(data, *args, **kwargs)
        except (TypeError, ValidationError):
            return {'msg': 'Invalid Content-Type header or JSON body'}, 400
    return wrapped

def validate_email(val: str) -> str:
    split = val.split('@')
    if (len(split) != 2 or split[0] == '' or split[1] == ''
    or len(val) < 8 or len(val) > 32):
        raise ValueError
    return val

def validate_password(val: str) -> str:
    if (not (search('[a-zA-Z]', val) and search('[0-9]', val))
    or len(val) < 8 or len(val) > 16):
        raise ValueError
    return val

def validate_name(val: str) -> str:
    if len(val) < 1 or len(val) > 16:
        raise ValueError
    return val
