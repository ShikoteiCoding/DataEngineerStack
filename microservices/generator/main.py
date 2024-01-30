import logging

from entrypoint import Session
from message import ProducerBuilder

from generator import Generator

if __name__ == "__main__":

    session = Session()

    env_config = session.config

    logger = logging.basicConfig(level=env_config["LOG_LEVEL"])

    definition_dict = session.definition_config

    message_builder = ProducerBuilder(definition_dict)
    message = message_builder.build()

    # build
    kafka_sink = session.sink
    kafka_sink.connect()

    generator = Generator(definition_dict, kafka_sink, message)
    generator.run()
