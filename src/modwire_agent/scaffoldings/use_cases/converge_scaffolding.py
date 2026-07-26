from dataclasses import dataclass
from typing import Any

from ..ports.outbound import ScaffoldingConvergence


@dataclass(frozen=True, slots=True)
class ConvergeScaffolding:
    convergence: ScaffoldingConvergence

    def execute(self, request: dict[str, Any]) -> dict[str, Any]:
        return self.convergence.execute(request)
