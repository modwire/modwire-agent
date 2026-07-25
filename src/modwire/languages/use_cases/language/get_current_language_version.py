from dataclasses import dataclass

from ...ports.language.version_reader import VersionReader
from .get_language import GetLanguage


@dataclass(frozen=True, slots=True)
class GetCurrentLanguageVersion:
    languages: GetLanguage
    versions: VersionReader

    def execute(self, language_id: str, timeout: float) -> str:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        return self.versions.read(self.languages.execute(language_id), timeout)
