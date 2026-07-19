from dataclasses import dataclass

from ...domain.contracts import Language, LanguageCatalog


@dataclass(frozen=True, slots=True)
class GetLanguage:
    catalog: LanguageCatalog

    def execute(self, language_id: str) -> Language:
        normalized = language_id.strip().lower()
        for language in self.catalog.languages:
            if language.id == normalized:
                return language
        raise LookupError(f"Unsupported language: {language_id}")
