from dataclasses import dataclass
from functools import partial
from typing import Callable

from functions import FUNCTIONS


def get_field_to_dict(msg: dict, field_path: list[str], func: Callable):
    if len(field_path) == 0:
        return
    if len(field_path) == 1:
        msg[field_path[0]] = func()

    key = field_path[0]
    field_path = field_path[1:]

    if not key in msg:
        msg[key] = {}

    get_field_to_dict(msg[key], field_path, func)
    return


@dataclass
class Field:
    name: str
    path: str
    type: str
    func: Callable


class Schema:
    def __init__(self, fields: list[Field]):
        self.fields = fields

    def generate_message(self) -> dict:
        msg = {}
        for field in self.fields:
            field_path = (field.path + "." if field.path else "") + field.name
            get_field_to_dict(msg, field_path.split("."), field.func)

        return msg


class SchemaBuilder:
    def __init__(self, definition: dict):
        self.definition_dict = definition

    def build(self) -> Schema:
        fields: list[Field] = []
        for field in self.definition_dict:

            if field["func"]:
                func_name: str = field["func"]["name"]
                func_params: list = field["func"].get("params", [])  # can not exist
                func = partial(FUNCTIONS[func_name], *func_params)
            else:
                func = partial(FUNCTIONS["type_value"], field["type"])

            field_params = {
                "name": field.get("name"),
                "path": field.get("path", ""),
                "type": field.get("type"),
                "func": func,
            }
            fields.append(Field(**field_params))

        return Schema(fields)
