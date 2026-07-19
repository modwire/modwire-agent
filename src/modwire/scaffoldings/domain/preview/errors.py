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


PreviewFailed = type(
    "PreviewFailed",
    (DomainError,),
    {"__init__": lambda self, errors: (setattr(self, "errors", errors), DomainError.__init__(self, "Scaffolding preview failed."))[1]},
)
