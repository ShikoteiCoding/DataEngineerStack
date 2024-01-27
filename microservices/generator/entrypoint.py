from __future__ import annotations

import json

from dataclasses import dataclass, field
from pathlib import Path
from ruamel.yaml import YAML
from sinks import Sink, ConsoleSink, KafkaSink
from config import Config


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
