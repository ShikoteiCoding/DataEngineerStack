import os
from dataclasses import dataclass, field
from typing import Callable, TypeAlias

@dataclass(slots=True)
class Config:
    collector_host: str | None = field(default=None)
    collector_port: str | None = field(default=None)

    def _collector_url(self) -> str:
        if self.collector_host and self.collector_port:
            return f"http://{self.collector_host}:{self.collector_port}"
        return ""

ConfigOptions: TypeAlias = Callable[[Config], None]

def load_conf(*opts: ConfigOptions) -> Config:
    """ Return a config according to  """
    c = Config()

    for opt in opts:
        opt(c)

    return c

def load_collector_opts(c: Config) -> None:
    """ Config for collector sink. """
    c.collector_host = os.getenv("COLLECTOR_HOST")
    c.collector_port = os.getenv("COLLECTOR_PORT")