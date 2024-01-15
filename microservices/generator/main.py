from dataclasses import dataclass
import logging

from config import Session
from definition import parse_definition_config
from message import MessageBuilder


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
