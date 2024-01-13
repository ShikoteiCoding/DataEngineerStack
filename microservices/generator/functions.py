from typing import Callable

def const_integer(val: int):
    return val

def type_value(type: str):
    if type == "dict":
        return {}
    elif type == "long":
        return 0
    elif type == "int":
        return 0
    elif type == "str":
        return ""

FUNCTIONS : dict[str, Callable] = {
    "const_integer": const_integer,
    "type_value": type_value
}