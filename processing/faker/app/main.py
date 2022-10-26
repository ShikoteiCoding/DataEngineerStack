import os
from typing import Callable
import requests
from config import load_conf as load, load_collector_opts, Config

import datetime
import time
import json

def stupid_generator():
    """ Simple generator. No variation, just reproducing """
    counter = 0
    while True:
        counter += 1
        yield {
            "body": {
                "timestamp": str(datetime.datetime.now()),
                "message": {
                    "metric": "TELEMETRY_MEASURE",
                    "value": 15
                },
                "count": counter
            }
        }
        time.sleep(2)

def faker_engine(c: Config, generator: Callable):
    """ Faker Engine goes here. """
    for data in generator():
        print(data)
        #res = requests.post(c._http_collector_url, json=data)
        #print(res)

if __name__ == "__main__":

    c = load(load_collector_opts)

    faker_engine(c, stupid_generator)