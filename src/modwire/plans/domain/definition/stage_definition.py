from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StageDefinition:
    identifier: str
    input_schema: dict[str, Any]
    submission_schema: dict[str, Any]
