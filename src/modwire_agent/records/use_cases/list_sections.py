from dataclasses import dataclass

from ..ports.outbound import SectionCatalog, SectionSummary


@dataclass(frozen=True, slots=True)
class ListSections:
    catalog: SectionCatalog

    def execute(self) -> list[SectionSummary]:
        return self.catalog.list()
