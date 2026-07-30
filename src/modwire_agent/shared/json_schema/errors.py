from dataclasses import dataclass

from modwire_agent.shared import DomainError


@dataclass(frozen=True, slots=True)
class JsonSchemaIssue:
    path: tuple[str | int, ...]
    message: str


class JsonSchemaError(DomainError):
    def __init__(self, issues: tuple[JsonSchemaIssue, ...]) -> None:
        self.issues = issues
        super().__init__("; ".join(issue.message for issue in issues))


class InvalidShape(JsonSchemaError):
    pass


class InvalidSchema(JsonSchemaError):
    pass


class InvalidValue(JsonSchemaError):
    pass
