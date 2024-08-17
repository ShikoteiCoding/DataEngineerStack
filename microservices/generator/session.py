from __future__ import annotations

import os

from typing import Self

from pathlib import Path
from sinks import Sink, ConsoleSink, KafkaSink
from config import Config
from dotenv import dotenv_values, load_dotenv
from ruamel.yaml import YAML

ROOT = Path().resolve()
GENERATOR_SUFFIX = Path("microservices/generator")
ENV_SUFFIX = Path("k8s/generator")
ENV_FILENAME = Path(".env")  # get renamed in volumes


class Session:
    def __init__(self):
        from_env = os.getenv("FROM_ENV", False)

        if not from_env:
            self.env_path: Path = ROOT.joinpath(ENV_SUFFIX).joinpath(
                ENV_FILENAME
            )  # read first to know current env setup
            load_dotenv(self.env_path)


        self.session_mode: str = os.getenv("ENV", "local")
        self._config: Config = Config({})
        self._definition: dict = {}

    def load_definition(self) -> Self:
        # might have multiple definition in the future.
        if not self._definition:
            folder_path = Path(self._config["FOLDER_DEFINITIONS"])
            self._definition = YAML().load(
                ROOT.joinpath(GENERATOR_SUFFIX).joinpath(folder_path)
            )
        return self

    def load_config(self) -> Self:
        """Load the config and make it available as a dict"""
        if not self._config:
            self._config = Config(dotenv_values(self.env_path))
            if self._config != {}:
                return self

        raise Exception(
            f"no environemnt variable set - {self.env_path} - {self.session_mode}"
        )

    @property
    def config(self) -> Config:
        return self._config

    @property
    def sink(self) -> Sink:
        """Load the sink used by generator."""
        sink_type = str(self._config.get("SINK_TYPE", "")).lower()

        match sink_type:
            case "console":
                return ConsoleSink(self._config)
            case "kafka":
                return KafkaSink(self._config)

        return Sink()

    @property
    def schema_definition(self) -> dict:
        """Load definition to build generator."""
        return self._definition["schema"]

    @property
    def generator_metadata(self) -> dict:
        return self._definition["generator"]
