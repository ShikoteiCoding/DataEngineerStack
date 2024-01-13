import logging
import requests
import datetime
import time

from typing import Callable
from pathlib import Path
from prometheus_client import start_http_server

from definition import parse_definition_config as load_definition

from message import SchemaBuilder


def stupid_generator():
    """ Simple generator. No variation, just reproducing """
    while True:
        yield {
            "body": {
                "timestamp": str(datetime.datetime.now()),
                "message": {
                    "metric": "TELEMETRY_MEASURE",
                    "value": 15
                }
            }
        }
        time.sleep(2)

def faker_engine(c: dict, generator: Callable):
    """ Faker Engine goes here. """
    for data in generator():
        logging.debug(f"Data generated: {data}")
        try:
            res = requests.post(c["output"]["api"]["endpoint"], json=data)
            logging.debug(f"Successfully posting to collector: {res}")
        except Exception as e:
            logging.error(f"Unreachable collector. {e}.")

class App:
    def run(self, *, output):
        ...

if __name__ == "__main__":
    # Metrics to get strapped
    start_http_server(8000)

    c = load_definition("configs/simple_generator.yaml")

    logging.basicConfig(level=c.log_level)

    # Set message builder from configuration

    m_bldr = SchemaBuilder(c["message"]["schema"])