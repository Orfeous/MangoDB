import json
from typing import Any, Dict

class JSONDecoder(json.JSONDecoder):
    _custom_types = {}

    @classmethod
    def register_type(cls, type_class: type) -> None:
        """Register a custom type for deserialization"""
        cls._custom_types[type_class.__name__] = type_class

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct: Dict[str, Any]) -> Any:
        """Convert JSON objects back to custom types"""
        if '__type__' in dct and dct['__type__'] in self._custom_types:
            type_class = self._custom_types[dct['__type__']]
            obj = type_class.__new__(type_class)
            obj.__dict__.update(dct['__value__'])
            return obj
        return dct
