from dataclasses import dataclass
import logging

from entrypoint import Session, KafkaSink
from definition import parse_definition_config
from message import ProducerBuilder

from generator import Generator


if __name__ == "__main__":

    session = Session(from_local=True)

    env_config = session.config

    logger = logging.basicConfig(level=env_config["LOG_LEVEL"])

    definition_path = "microservices/generator/definitions/simple_generator.yaml"
    definition_dict = parse_definition_config(definition_path)

    message_builder = ProducerBuilder(definition_dict)
    message = message_builder.build()

    # build
    kafka_sink = session.sink
    kafka_sink.connect()

    generator = Generator(definition_dict, kafka_sink, message)

    generator.run()
