import os
import logging
import requests

import datetime
import time
import json

from typing import Callable
from config import load_conf as load, load_collector_opts, Config


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

def faker_engine(c: Config, generator: Callable):
    """ Faker Engine goes here. """
    for data in generator():
        logging.debug(f"Data generated: {data}")
        try:
            res = requests.post(c._http_collector_url, json=data)
            logging.debug(f"Successfully posting to collector: {res}")
        except Exception as e:
            logging.error(f"Unreachable collector. {e}.")
        

if __name__ == "__main__":

    c = load(load_collector_opts)

    logging.basicConfig(level=c.log_level)

    faker_engine(c, stupid_generator)