from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PreviewError:
    code: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

    def as_dict(self):
        result = {"code": self.code, "message": self.message}
        if self.context:
            result["details"] = self.context
        return result


class PreviewFailed(Exception):
    def __init__(self, errors: list[PreviewError]):
        self.errors = errors
        super().__init__("Scaffolding preview failed.")
