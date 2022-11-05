from dataclasses import make_dataclass

from jsonpath_ng import Root

class Schema:
    ...

class SchemaBuilder:
    def __init__(self, definition):
        self.definition = definition
        self.schema = {}
        

    def _parse_definition(self):
        ...

    def _make_message(self):
        type_map = {
            "int": int,
            "string": str,
            "dict": dict
        }
        return make_dataclass(
            "Message",
            [(e["name"], type_map.get(e["type"], str)) for e in self.definition],
        )

    def build(self) -> Schema:
        ...

#class Message:
#    ...