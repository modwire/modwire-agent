from dataclasses import dataclass
from typing import Any

from ..ports.outbound import ScaffoldingCatalog


@dataclass(frozen=True, slots=True)
class GetScaffolding:
    catalog: ScaffoldingCatalog

    def execute(self, identifier: str) -> Any:
        return self.catalog.get(identifier)
