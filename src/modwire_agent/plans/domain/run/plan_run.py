from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from .plan_run_status import PlanRunStatus


@dataclass(frozen=True, slots=True)
class PlanRun:
    identifier: UUID
    definition_id: UUID
    definition_version: int
    current_stage_id: str
    current_input: dict[str, Any]
    status: PlanRunStatus
    revision: int

    def advance(self, stage_id: str, stage_input: dict[str, Any]) -> PlanRun:
        return PlanRun(
            self.identifier,
            self.definition_id,
            self.definition_version,
            stage_id,
            stage_input,
            PlanRunStatus.ACTIVE,
            self.revision + 1,
        )

    def complete(self) -> PlanRun:
        return PlanRun(
            self.identifier,
            self.definition_id,
            self.definition_version,
            self.current_stage_id,
            self.current_input,
            PlanRunStatus.COMPLETE,
            self.revision + 1,
        )
