import logging
import requests
import datetime
import time

from typing import Callable
from pathlib import Path
from prometheus_client import start_http_server

from config import load as load_config


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

if __name__ == "__main__":
    # Metrics to get strapped
    start_http_server(8000)

    c = load_config(Path("configs/mygenerator.yaml"))

    logging.basicConfig(level=c.log_level)

    faker_engine(c, stupid_generator)