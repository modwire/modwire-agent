from dataclasses import dataclass, field
from typing import Any

from modwire_hex import DomainError


@dataclass(frozen=True, slots=True)
class PreviewError:
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.context:
            result["details"] = self.context
        return result


class PreviewFailed(DomainError):
    def __init__(self, errors: list[PreviewError]):
        self.errors = errors
        super().__init__("Scaffolding preview failed.")
