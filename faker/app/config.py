import os
from dataclasses import dataclass, field
from typing import Callable, TypeAlias

@dataclass(slots=True)
class Config:
    collector_url: str | None = field(default=None)

ConfigOptions: TypeAlias = Callable[[Config], None]

def load_conf(*opts: ConfigOptions) -> Config:
    """ Return a config according to  """
    c = Config()

    for opt in opts:
        opt(c)

    return c

def load_collector_opts(c: Config) -> None:
    """ Config for collector sink. """
    c.collector_url = os.getenv("COLLECTOR_ENDPOINT")