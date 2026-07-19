from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...use_cases.run.start_plan_run import StartPlanRun
from .schemas.plan_run_input import PlanRunInput
from .schemas.plan_run_output import PlanRunOutput


@api_controller("/plans/runs", tags=["plans"])
class StartPlanRunController(ControllerBase):
    @route.post("", response={201: PlanRunOutput}, operation_id="start_plan_run")
    def start(self, request: Any, payload: PlanRunInput) -> tuple[int, PlanRunOutput]:
        try:
            run = DjangoRequest.resolve(request, StartPlanRun).execute(UUID(payload.definition_id), payload.initial_input)
        except (InvalidStageSubmission, LookupError, ValueError) as error:
            raise HttpError(422, str(error)) from error
        return 201, PlanRunOutput(id=str(run.identifier), current_stage_id=run.current_stage_id, status=run.status)
