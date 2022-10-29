import os
from dataclasses import dataclass, field
from typing import Callable, TypeAlias

from os import getenv
from pathlib import Path
from ruamel.yaml import YAML

def load(stream:Path|str=Path(getenv("PIPELINE_CONF", "messages/mygenerator.yaml"))):
    """ Load config to build generator. """
    # Read pipeline configuration as a YAML file
    config = YAML().load(stream)

    # Set globals settings from env
    config.log_level = getenv("LOG_LEVEL", "DEBUG").upper()

    return config