from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class StageSubmission:
    identifier: UUID
    plan_run_id: UUID
    stage_id: str
    payload: dict[str, Any]
