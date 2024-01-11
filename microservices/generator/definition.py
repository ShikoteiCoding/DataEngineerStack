from dataclasses import dataclass, field

from pathlib import Path
from ruamel.yaml import YAML
from collections import OrderedDict

def load(path: str):
    """ Load definition to build generator. """
    definition = YAML().load(Path(path))

    return definition