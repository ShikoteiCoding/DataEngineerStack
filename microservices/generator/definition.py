from dataclasses import dataclass, field

from pathlib import Path
from ruamel.yaml import YAML


def parse_definition_config(path: str) -> dict:
    """Load definition to build generator."""
    definition = YAML().load(Path(path))

    return definition
