import json
from typing import Any

class JSONEncoder(json.JSONEncoder):
    _custom_types = {}

    @classmethod
    def register_type(cls, type_class: type) -> None:
        """Register a custom type for serialization"""
        cls._custom_types[type_class.__name__] = type_class

    def default(self, obj: Any) -> Any:
        """Convert custom types to JSON-serializable format"""
        if type(obj) in self._custom_types.values():
            return {
                '__type__': type(obj).__name__,
                '__value__': obj.__dict__
            }
        return super().default(obj)
