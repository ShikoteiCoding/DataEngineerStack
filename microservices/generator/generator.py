from message import Schema
from entrypoint import Sink

from isodate import parse_duration
from datetime import timedelta

import time


class Generator:
    def __init__(self, definition: dict, sink: Sink, message: Schema):
        self.sink = sink
        self.message = message
        self.parse_definition(definition)
        self._interval: timedelta

    @property
    def interval(self) -> int:
        return int(self._interval.total_seconds())

    def parse_definition(self, definition: dict):
        interval: str = definition["interval"]
        self._interval = parse_duration(interval)

    def run(self):

        while True:
            self.sink.post(self.message, topic="test")
            time.sleep(self.interval)
