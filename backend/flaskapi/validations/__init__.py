from typing import Callable
from functools import wraps
from re import search
from pydantic import (
    BaseModel,
    ValidationError
)
from flask import (
    request,
    jsonify
)

def validate_json(schema: BaseModel):
    def decorator(func: Callable):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                data = schema.model_validate(request.get_json(silent=True))
            except (TypeError, ValidationError):
                return jsonify(
                    {'msg': 'Invalid Content-Type header or JSON body'}
                ), 400    
            return func(data, *args, **kwargs)
        return wrapped
    return decorator

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
