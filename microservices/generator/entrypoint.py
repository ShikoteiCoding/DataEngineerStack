from __future__ import annotations

import os
import socket

from dataclasses import dataclass, field
from pathlib import Path
from ruamel.yaml import YAML
from message import ProducerMessage
from confluent_kafka import Producer
from typing import Any


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


class Sink:
    def test_connection(self):
        ...

    def connect(self):
        print(f"connecting to default Sink...")

    def post(self, producer: ProducerMessage):
        ...


class KafkaSink(Sink):
    def __init__(self, config: Config):
        self.config = config

    def connect(self):
        conf = self.config.kafka_conf
        print(f"connecting to kafka with conf {conf}...")
        self.producer: Producer = Producer(conf)

    def post(self, producer: ProducerMessage, topic: str = ""):
        self.producer.produce(topic, key="key", value="value", callback=acked)


class ConsoleSink(Sink):
    def __init__(self, config: Config):
        self.config = config

    def post(self, producer: ProducerMessage):
        print(producer.generate_message())


class Config(dict):
    def __init__(self, config: dict):
        super().__init__(config)
    
    @property
    def kafka_conf(self) -> dict:
        conf = {
            "bootstrap.servers": self.get("KAFKA_BOOTSTRAP_SERVERS"),
        }
        return conf
    
    def __getitem__(self, __key: Any, __default: Any = None) -> Any:
        return self.get(__key, __default)


@dataclass
class Session:
    from_local: bool = field(default=False)
    config_path: str = field(default="microservices/generator/config.yaml")

    @property
    def config(self) -> Config:
        if self.from_local:
            self._config: Config = Config(YAML().load(Path(self.config_path)))
        else:
            self._config: Config = Config({})  # TODO: read from env
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
