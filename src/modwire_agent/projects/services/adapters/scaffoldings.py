from dataclasses import dataclass

from wireup import injectable

from modwire_agent.scaffoldings.services import ScaffoldingService


@injectable
@dataclass(frozen=True)
class ScaffoldingsAdapter:
    scaffoldings: ScaffoldingService

    def check_scaffolding_existence(self, scaffolding_id: str) -> None:
        self.scaffoldings.get(scaffolding_id)
