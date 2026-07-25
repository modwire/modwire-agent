from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ...use_cases.operation.execute_stage_operation import ExecuteStageOperation


@api_controller("/plans/runs", tags=["plans"])
class ExecuteStageOperationController(ControllerBase):
    @route.post("/{run_id}/operations/{operation_id}", response={204: None}, operation_id="execute_plan_run_operation")
    def execute(self, request: Any, run_id: UUID, operation_id: str) -> int:
        """Execute an available operation for the active plan stage."""
        DjangoRequest.resolve(request, ExecuteStageOperation).execute(run_id, operation_id)
        return 204
