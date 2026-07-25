from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.gate.gate_satisfaction import GateSatisfaction


class GateSatisfactionStore(ABC):
    @abstractmethod
    def find(self, run_id: UUID, gate_id: str) -> GateSatisfaction | None:
        raise NotImplementedError

    @abstractmethod
    def satisfied_gate_ids(self, run_id: UUID) -> set[str]:
        raise NotImplementedError

    @abstractmethod
    def save(self, satisfaction: GateSatisfaction) -> None:
        raise NotImplementedError
