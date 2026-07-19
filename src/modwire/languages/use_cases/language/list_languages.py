from dataclasses import dataclass

from ...domain.contracts import Language, LanguageCatalog


@dataclass(frozen=True, slots=True)
class ListLanguages:
    catalog: LanguageCatalog

    def execute(self) -> tuple[Language, ...]:
        return self.catalog.languages
