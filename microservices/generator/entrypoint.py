import os
from dataclasses import dataclass, field

from pathlib import Path
from ruamel.yaml import YAML
from message import Producer


class Sink:
    def test_connection(self):
        ...

    def connect(self):
        ...

    def post(self, producer: Producer):
        ...


class KafkaSink(Sink):
    def __init__(self, config: dict):
        self.config = config

    def connect(self):
        print("connecting to kafka...")

    def post(self, producer: Producer):
        print(producer.generate_message())


class ConsoleSink(Sink):
    def __init__(self, config: dict):
        self.config = config

    def post(self, producer: Producer):
        print(producer.generate_message())


@dataclass
class Session:
    from_local: bool = field(default=False)
    config_path: str = field(default="microservices/generator/config.yaml")
    _config: dict = field(default_factory=dict)

    @property
    def config(self) -> dict:
        if self.from_local:
            self._config: dict = YAML().load(Path(self.config_path))
        else:
            self._config: dict = {}  # TODO: read from env
        return self._config

    @property
    def sink(self) -> Sink:
        sink_type = str(self._config.get("SINK_TYPE", "")).lower()

        match sink_type:
            case "console":
                return ConsoleSink(self._config)
            case "kafka":
                return KafkaSink(self._config)

        return Sink()
