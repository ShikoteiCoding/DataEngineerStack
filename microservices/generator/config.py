import os
from dataclasses import dataclass, field
from typing import Callable, TypeAlias

from os import getenv
from pathlib import Path
from ruamel.yaml import YAML


@dataclass
class Session:
    from_local: bool = field(default=False)
    config_path: str = field(default="microservices/generator/config.yaml")

    @property
    def config(self) -> dict[str, str]:
        if self.from_local:
            c: dict = YAML().load(Path(self.config_path))
        else:
            c: dict = {} # TODO: read from env
        return c