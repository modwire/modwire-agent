from dataclasses import dataclass
from typing import Any

from ..ports.variable_catalog import VariableCatalog


@dataclass(frozen=True, slots=True)
class VariableService:
    catalog: VariableCatalog

    def get(self, identifier: str) -> Any:
        return self.catalog.get(identifier)
