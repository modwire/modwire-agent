from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SectionSummary:
    identifier: UUID
    title: str
    allowed_kinds: tuple[str, ...]


class SectionCatalog(ABC):
    @abstractmethod
    def list(self) -> list[SectionSummary]:
        raise NotImplementedError
