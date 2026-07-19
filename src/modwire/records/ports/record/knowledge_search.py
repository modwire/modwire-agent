from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class SearchResult:
    identifier: UUID
    title: str
    reason: str


class KnowledgeSearch(ABC):
    @abstractmethod
    def semantic(self, query: str) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    def text(self, query: str) -> list[SearchResult]:
        raise NotImplementedError
