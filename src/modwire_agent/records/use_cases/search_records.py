from dataclasses import dataclass

from ..ports.outbound import KnowledgeSearch, SearchResult


@dataclass(frozen=True, slots=True)
class SearchRecords:
    search: KnowledgeSearch

    def semantic(self, query: str) -> list[SearchResult]:
        return self.search.semantic(query)

    def text(self, query: str) -> list[SearchResult]:
        return self.search.text(query)
