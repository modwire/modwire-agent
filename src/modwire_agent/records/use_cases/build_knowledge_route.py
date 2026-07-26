from dataclasses import dataclass

from ..ports.outbound import KnowledgeRouter, RoutedRecord


@dataclass(frozen=True, slots=True)
class BuildKnowledgeRoute:
    router: KnowledgeRouter

    def execute(self, tags: list[str]) -> list[RoutedRecord]:
        return self.router.route(tags)
