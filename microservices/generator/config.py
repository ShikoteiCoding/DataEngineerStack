from typing import Any

class Config(dict):
    def __init__(self, config: dict):
        super().__init__(config)

    @property
    def kafka_conf(self) -> dict:
        conf = {
            "bootstrap.servers": self.get("KAFKA_BOOTSTRAP_SERVERS"),
        }
        return conf

    def __getitem__(self, __key: Any, __default: Any = None) -> Any:
        return self.get(__key, __default)