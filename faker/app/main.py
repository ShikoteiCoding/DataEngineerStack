import os
from typing import Callable
import requests
from config import load_conf as load, load_collector_opts, Config

import datetime
import time
import json

def stupid_generator() -> dict:
    """ Simple generator. No variation, just reproducing """
    time.sleep(2)
    return {
        "body": {
            "timestamp": str(datetime.datetime.now()),
            "message": {
                "metric": "TELEMETRY_MEASURE",
                "vale": 15
            }
        }
    }

def faker_engine(c: Config, generator: Callable):
    """ Faker Engine goes here. """
    while True:
        data = generator()
        res = requests.post(c._collector_url, json=data)
        print(res)

if __name__ == "__main__":

    c = load(load_collector_opts)

    faker_engine(c, stupid_generator)