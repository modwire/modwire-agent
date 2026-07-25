from abc import ABC, abstractmethod
from typing import Any


class SchemaValidator(ABC):
    @abstractmethod
    def require_valid_schema(self, schema: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def require_valid_value(self, schema: dict[str, Any], value: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def require_compatible_values(self, output_schema: dict[str, Any], input_schema: dict[str, Any]) -> None:
        raise NotImplementedError
