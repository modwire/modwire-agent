from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.run.plan_run import PlanRun


class PlanRunStore(ABC):
    @abstractmethod
    def get(self, run_id: UUID) -> PlanRun:
        raise NotImplementedError

    @abstractmethod
    def save(self, run: PlanRun) -> None:
        raise NotImplementedError
