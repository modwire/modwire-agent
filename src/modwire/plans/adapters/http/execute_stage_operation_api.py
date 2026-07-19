from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from ...domain.definition.invalid_plan_definition import InvalidPlanDefinition
from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...use_cases.operation.execute_stage_operation import ExecuteStageOperation


@api_controller("/plans/runs", tags=["plans"])
class ExecuteStageOperationController(ControllerBase):
    @route.post("/{run_id}/operations/{operation_id}", response={204: None})
    def execute(self, request: Any, run_id: UUID, operation_id: str) -> int:
        try:
            DjangoRequest.resolve(request, ExecuteStageOperation).execute(run_id, operation_id)
        except (InvalidPlanDefinition, InvalidStageSubmission, LookupError) as error:
            raise HttpError(422, str(error)) from error
        return 204
