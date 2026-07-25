from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GateSatisfaction:
    identifier: UUID
    plan_run_id: UUID
    gate_id: str
    evidence: dict[str, Any]
