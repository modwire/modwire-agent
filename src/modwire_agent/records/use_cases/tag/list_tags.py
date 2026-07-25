from dataclasses import dataclass

from ...ports.tag.tag_catalog import TagCatalog, TagSummary


@dataclass(frozen=True, slots=True)
class ListTags:
    catalog: TagCatalog

    def execute(self) -> list[TagSummary]:
        return self.catalog.list()
