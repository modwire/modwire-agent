from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class JsonSchemaIssue:
    path: tuple[str | int, ...]
    message: str


class JsonSchemaError(ValueError):
    def __init__(self, issues: tuple[JsonSchemaIssue, ...]) -> None:
        self.issues = issues
        super().__init__("; ".join(issue.message for issue in issues))


class InvalidShape(JsonSchemaError):
    pass


class InvalidSchema(JsonSchemaError):
    pass


class InvalidValue(JsonSchemaError):
    pass
