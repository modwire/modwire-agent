from dataclasses import dataclass

from wireup import injectable

from modwire_agent.shared import DomainError, LanguagesService

from ...errors import RecordsError


@injectable
@dataclass(frozen=True)
class ResourceValidator:
    languages: LanguagesService

    def validate(self, language: str, path: str, content: str) -> None:
        try:
            self.languages.validate_source(language, path, content)
        except DomainError as error:
            raise RecordsError(str(error)) from error
