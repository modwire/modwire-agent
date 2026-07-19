from dataclasses import dataclass

from ..domain.contracts import Language, LanguageCatalog
from ..ports.version_reader import VersionReader


@dataclass(frozen=True, slots=True)
class LanguageCatalogService:
    catalog: LanguageCatalog
    versions: VersionReader

    def find_all(self) -> tuple[Language, ...]:
        return self.catalog.languages

    def find(self, language_id: str) -> Language:
        normalized = language_id.strip().lower()
        for language in self.catalog.languages:
            if language.id == normalized:
                return language
        raise ValueError(f"Unsupported language: {language_id}")

    def find_current_version(self, language_id: str, timeout: float = 10) -> str:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        return self.versions.read(self.find(language_id), timeout)
