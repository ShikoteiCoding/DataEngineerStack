from message import ProducerMessage
from entrypoint import Sink

from isodate import parse_duration

import time


class Generator:
    def __init__(self, definition: dict, sink: Sink, message: ProducerMessage):
        self.sink = sink
        self.message = message
        self.parse_definition(definition)

    @property
    def interval(self) -> int:
        return int(self._interval.total_seconds())

    def parse_definition(self, definition: dict):
        interval: str = definition["generator"]["interval"]
        self._interval = parse_duration(interval)

    def run(self):

        while True:
            self.sink.post(self.message)
            time.sleep(self.interval)
