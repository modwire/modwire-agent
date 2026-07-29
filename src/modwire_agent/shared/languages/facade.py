from collections.abc import Sequence
from dataclasses import dataclass

from .base import Language


@dataclass(frozen=True)
class LanguagesService:
    languages: Sequence[Language]

    def get_extensions(self, language: str) -> list[str]:
        for supported_language in self.languages:
            if supported_language.id == language:
                return list(supported_language.source_extensions)
        raise ValueError(f"Unsupported language ID: {language!r}")

    def get_ids(self) -> list[str]:
        return [language.id for language in self.languages]
