from typing import Any
from uuid import uuid4

from ..definition.plan_definition import PlanDefinition
from .plan_run import PlanRun
from .plan_run_status import PlanRunStatus
from .stage_submission import StageSubmission
from .stage_transition import StageTransition


class PlanRunPolicy:
    def start(self, definition: PlanDefinition, initial_input: dict[str, Any]) -> PlanRun:
        return PlanRun(uuid4(), definition.identifier, definition.version, definition.start_stage_id, initial_input, PlanRunStatus.ACTIVE, 0)

    def advance(self, run: PlanRun, next_stage_id: str, payload: dict[str, Any]) -> PlanRun:
        if not next_stage_id:
            return run.complete()
        return run.advance(next_stage_id, payload)

    def transition(self, run: PlanRun, next_stage_id: str, payload: dict[str, Any]) -> StageTransition:
        return StageTransition(StageSubmission(uuid4(), run.identifier, run.current_stage_id, payload), self.advance(run, next_stage_id, payload), run.revision)
