from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RoutedRecord:
    identifier: UUID
    title: str
    matched_tag: str | None


class KnowledgeRouter(ABC):
    @abstractmethod
    def route(self, tag_names: list[str]) -> list[RoutedRecord]:
        raise NotImplementedError
