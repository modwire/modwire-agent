from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class TagSummary:
    identifier: UUID
    name: str


class TagCatalog(ABC):
    @abstractmethod
    def list(self) -> list[TagSummary]:
        raise NotImplementedError
