import os
from dataclasses import dataclass, field

from pathlib import Path
from ruamel.yaml import YAML
from message import Producer


class Sink:

    def test_connection(self): ...
        
    def connect(self): ...

    def post(self, producer: Producer): ...

class KafkaSink(Sink):
    
    def __init__(self, config: dict):
        self.config = config

    def connect(self):
        print("connecting to kafka...")

    def post(self, producer: Producer):
        print(producer.generate_message())

@dataclass
class Session:
    from_local: bool = field(default=False)
    config_path: str = field(default="microservices/generator/config.yaml")

    @property
    def config(self) -> dict[str, str]:
        if self.from_local:
            c: dict = YAML().load(Path(self.config_path))
        else:
            c: dict = {}  # TODO: read from env
        return c
    
    @property
    def sink(self) -> Sink:
        return Sink()
