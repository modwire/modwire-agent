from collections.abc import Sequence
from dataclasses import dataclass

from wireup import injectable

from modwire_agent.shared import DiagramsService

from ..source_code.extraction import SourceExtractionService
from .base import Language
from .errors import LanguagesError


@injectable
@dataclass(frozen=True)
class LanguagesService:
    languages: Sequence[Language]
    extraction: SourceExtractionService
    diagrams: DiagramsService

    def get_extensions(self, language: str) -> list[str]:
        return list(self._get(language).source_extensions)

    def get_ids(self) -> list[str]:
        return [language.id for language in self.languages]

    def validate_source(self, language: str, path: str, content: str) -> None:
        supported_language = self._get(language)
        extensions = supported_language.source_extensions

        if not path.endswith(tuple(extensions)):
            raise LanguagesError(f"Source path {path!r} not match {language!r}.")

        supported_language.validate(path, content)
        if language == "mermaid":
            self.diagrams.recognize(content)

        if supported_language.requires_extraction:
            self.extraction.validate(supported_language.id, path, content)

    def _get(self, language: str) -> Language:
        for supported_language in self.languages:
            if supported_language.id == language:
                return supported_language
        raise LanguagesError(f"Unsupported language ID: {language!r}")
