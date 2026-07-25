from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.definition.plan_definition import PlanDefinition


class PlanDefinitionStore(ABC):
    @abstractmethod
    def get(self, definition_id: UUID) -> PlanDefinition:
        raise NotImplementedError

    @abstractmethod
    def next_version(self, name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def publish(self, definition: PlanDefinition) -> None:
        raise NotImplementedError
