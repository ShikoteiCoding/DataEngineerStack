from dataclasses import dataclass
import logging

from typing import Callable
from functools import partial

from config import Session
from definition import parse_definition_config
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


class Message:
    def __init__(self, fields: list[Field]):
        self.fields = fields

    

    def get_json(self) -> dict:
        msg = {}
        for field in self.fields:
            field_path = (field.path + "." if field.path else "") + field.name
            get_field_to_dict(msg, field_path.split("."), field.func)
            
        return msg


class MessageBuilder:

    def __init__(self, definition_dict: dict):
        self.definition_dict = definition_dict

    def build(self):
        fields: list[Field] = []
        for field in definition_dict["message"]["schema"]:
            print(field)

            if field.get("func"):
                func_name: str = field.get("func").get("name")
                func_params: list = field.get("func").get("params", [])
                print(func_name, func_params)
                func = partial(FUNCTIONS.get(func_name), *func_params) #type: ignore
            else:
                func = partial(FUNCTIONS.get("type_value"), field.get("type")) #type: ignore

            field_params = {
                "name": field.get("name"),
                "path": field.get("path", ""),
                "type": field.get("type"),
                "func": func
            }
            fields.append(Field(**field_params))

        return Message(fields)



if __name__ == "__main__":
    
    session = Session(from_local=True)

    env_config = session.config

    logger = logging.basicConfig(level=env_config["LOG_LEVEL"])

    definition_path = "microservices/generator/definitions/simple_generator.yaml"
    definition_dict = parse_definition_config(definition_path)

    message_builder = MessageBuilder(definition_dict)
    message = message_builder.build()
    msg = message.get_json()
    print(msg)
    