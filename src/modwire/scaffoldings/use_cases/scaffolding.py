from dataclasses import dataclass
from typing import Any

from ..ports.scaffolding_catalog import ScaffoldingCatalog


@dataclass(frozen=True, slots=True)
class ScaffoldingService:
    catalog: ScaffoldingCatalog

    def get(self, identifier: str) -> Any:
        return self.catalog.get(identifier)
