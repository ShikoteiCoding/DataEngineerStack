import logging

from entrypoint import Session
from message import SchemaBuilder

from generator import Generator

if __name__ == "__main__":

    session = Session().load_config().load_definition()

    logger = logging.basicConfig(level=session.config["LOG_LEVEL"])

    schema = SchemaBuilder(session.schema_definition).build()

    # build
    sink = session.sink
    sink.connect()

    generator = Generator(session.generator_metadata, sink, schema)
    generator.run()
