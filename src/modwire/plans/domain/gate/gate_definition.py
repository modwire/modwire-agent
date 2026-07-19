from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class GateDefinition:
    identifier: str
    stage_id: str
    evidence_schema: dict[str, Any]
