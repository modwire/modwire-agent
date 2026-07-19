import json
from dataclasses import dataclass
from urllib.request import Request, urlopen


from .contracts import Language, LanguageCatalog


class LanguageVersionError(RuntimeError):
    pass


@dataclass(frozen=True)
class LanguageVersionService:
    def find_current(self, language: Language, timeout: float = 10) -> str:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        request = Request(
            language.version_provider.url,
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )
        try:
            with urlopen(request, timeout=timeout) as response:  # noqa: S310
                version = self._extract(json.load(response), language)
        except (OSError, ValueError, IndexError, KeyError, TypeError) as error:
            raise LanguageVersionError(f"Could not obtain the current {language.name} version: {error}") from error
        if not isinstance(version, str) or not version:
            raise LanguageVersionError(f"The version provider returned an invalid current {language.name} version.")
        return version

    @staticmethod
    def _extract(data, language: Language) -> str:
        value = data
        for item in language.version_provider.result_path:
            value = value[item]
        return value


@dataclass(frozen=True)
class LanguageCatalogService:
    catalog: LanguageCatalog
    versions: LanguageVersionService

    def find_all(self) -> tuple[Language, ...]:
        return self.catalog.languages

    def find(self, language_id: str) -> Language:
        normalized = language_id.strip().lower()
        for language in self.catalog.languages:
            if language.id == normalized:
                return language
        raise ValueError(f"Unsupported language: {language_id}")

    def find_current_version(self, language_id: str, timeout: float = 10) -> str:
        return self.versions.find_current(self.find(language_id), timeout)
