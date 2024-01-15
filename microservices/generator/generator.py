from message import Producer
from entrypoint import Sink

class Generator:

    def __init__(self, sink: Sink, message: Producer):
        self.sink = sink
        self.message = message

    def run(self):
        self.sink.post(self.message)