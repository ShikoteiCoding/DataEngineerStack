from __future__ import annotations

import os

from pathlib import Path
from sinks import Sink, ConsoleSink, KafkaSink
from config import Config
from dotenv import dotenv_values, load_dotenv
from ruamel.yaml import YAML

ROOT = Path().resolve()
GENERATOR_SUFFIX = Path("microservices/generator")
ENV_SUFFIX = Path("k8s/generator")
ENV_FILENAME = Path(".env") # get renamed in volumes

class Session:

    def __init__(self):
        self.env_path = ROOT.joinpath(ENV_SUFFIX).joinpath(ENV_FILENAME) # read first to know current env setup
        load_dotenv(self.env_path)
        self.session_mode: str = os.getenv("ENV", "local")
        self._config = Config({})

    @property
    def config(self) -> Config:
        """Load the config and make it available as a dict"""
        self._config = Config(dotenv_values(self.env_path))
        if self._config != {}:
            return self._config
        
        raise Exception(f"no environemnt variable set - {self.env_path} - {self.session_mode}")

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
    def definition_config(self) -> dict:
        """Load definition to build generator."""
        folder_path = Path(self._config["FOLDER_DEFINITIONS"])
        definition = YAML().load(
            ROOT.joinpath(GENERATOR_SUFFIX).joinpath(folder_path)
        )

        return definition

