from re import search

def validate_email(val: str) -> None:
    split = val.split('@')
    if (len(split) != 2 or split[0] == '' or split[1] == ''
    or len(val) < 8 or len(val) > 32):
        raise ValueError

def validate_password(val: str) -> None:
    if (not (search('[a-zA-Z]', val) and search('[0-9]', val))
    or len(val) < 8 or len(val) > 16):
        raise ValueError

def validate_name(val: str) -> None:
    if len(val) < 1 or len(val) > 16:
        raise ValueError
