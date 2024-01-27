from dateutil.parser import parse
from typing import Callable
from datetime import datetime, timezone

def const_datetime(val: str) -> str:
    """parse str as string"""
    return parse(val).strftime('%s')


def const_integer(val: int) -> int:
    return val


def const_str(val: str) -> str:
    return val


def now() -> str: # datetime not json convertible, store it as 
    return datetime.now(tz=timezone.utc).strftime('%s')


def type_value(type: str):
    if type == "dict":
        return {}
    elif type == "long":
        return 0
    elif type == "int":
        return 0
    elif type == "str":
        return ""
    elif type == "datetime":
        return ""


FUNCTIONS: dict[str, Callable] = {
    "const_integer": const_integer,
    "const_str": const_str,
    "now": now,
    "type_value": type_value,
}
