from typing import Any, LiteralString
from collections.abc import Callable
from functools import wraps
from re import fullmatch
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticCustomError
from flask import Response, jsonify, request
from werkzeug.exceptions import UnsupportedMediaType, BadRequest

type EndpointFunc = Callable[..., tuple[Response, int]]

def validate_json(func: EndpointFunc) -> EndpointFunc:
    Schema: type[BaseModel] = func.__annotations__['data']
    @wraps(func)
    def decorated(*args, **kwargs) -> tuple[Response, int]:
        try:
            data: BaseModel = Schema.model_validate(request.get_json())
        except UnsupportedMediaType:
            return jsonify(msg='Invalid Content-Type header'), 415
        except BadRequest:
            return jsonify(msg='Invalid JSON body syntax'), 400
        except ValidationError as e:
            errors: list[dict[str, Any]] = [
                {key: error[key] for key in ('input', 'loc', 'msg')}
                for error in e.errors()
            ]
            return jsonify(msg='Validation failed', errors=errors), 422
        return func(data, *args, **kwargs)
    return decorated

def lower_str(validate_func: Callable[[str], str]) -> Callable[[str], str]:
    def _lower_str(val: str) -> str:
        return validate_func(val).lower()
    return _lower_str

def validate_str(regex: str, message: LiteralString) -> Callable[[str], str]:
    def _validate_str(val: str) -> str:
        if not fullmatch(regex, val):
            raise PydanticCustomError('value_error', message)
        return val
    return _validate_str

validate_email: Callable[[str], str] = validate_str(
    r'^(?=.{6,100}$)[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'Email must be 6-100 characters and in a standard email format'
)
validate_password: Callable[[str], str] = validate_str(
    r'^(?=.{15,75}$)(?=.*[a-zA-Z])(?=.*[0-9])[\x21-\x7E]+$',
    'Password must be 15-75 characters and include letters and numbers'
)
validate_name: Callable[[str], str] = validate_str(
    r'^.{1,30}$', 'Name must be 1-30 characters'
)
