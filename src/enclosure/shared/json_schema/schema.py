from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .validator import JsonSchemaValidator


@dataclass(frozen=True)
class Schema:
    _document: dict[str, Any]
    _validator: JsonSchemaValidator

    def __post_init__(self) -> None:
        object.__setattr__(self, "_document", deepcopy(self._document))

    @property
    def document(self) -> dict[str, Any]:
        return deepcopy(self._document)

    def require_valid(self, value: Any) -> None:
        self._validator.require_valid_value(self._document, value)
