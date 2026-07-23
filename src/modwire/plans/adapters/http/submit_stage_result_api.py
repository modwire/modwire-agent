from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ...use_cases.run.submit_stage_result import SubmitStageResult
from .schemas.plan_run_output import PlanRunOutput
from .schemas.stage_submission_input import StageSubmissionInput


@api_controller("/plans/runs", tags=["plans"])
class SubmitStageResultController(ControllerBase):
    @route.post("/{run_id}/submissions", response={200: PlanRunOutput}, operation_id="submit_stage_result")
    def submit(self, request: Any, run_id: UUID, payload: StageSubmissionInput) -> tuple[int, PlanRunOutput]:
        run = DjangoRequest.resolve(request, SubmitStageResult).execute(run_id, payload.payload)
        return 200, PlanRunOutput(id=str(run.identifier), current_stage_id=run.current_stage_id, status=run.status)
