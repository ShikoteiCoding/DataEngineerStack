import os
from dataclasses import dataclass, field
from typing import Callable, TypeAlias

@dataclass(slots=True)
class Config:
    collector_url: str = field(default="")

    @property
    def _http_collector_url(self) -> str:
        if self.collector_url:
            return f"http://{self.collector_url}"
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
    c.collector_url = os.getenv("COLLECTOR_URL", "").replace("http://", "")