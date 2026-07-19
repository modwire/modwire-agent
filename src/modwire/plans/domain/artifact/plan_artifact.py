from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class PlanArtifact:
    identifier: UUID
    plan_run_id: UUID
    artifact_id: str
    payload: dict[str, Any]
