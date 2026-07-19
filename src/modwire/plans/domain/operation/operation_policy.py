from typing import Any
from uuid import UUID, uuid4

from ..definition.invalid_plan_definition import InvalidPlanDefinition
from ..definition.plan_definition import PlanDefinition
from .operation_claim import OperationClaim
from .operation_execution import OperationExecution


class OperationPolicy:
    def get(self, definition: PlanDefinition, operation_id: str):
        for operation in definition.operations:
            if operation.identifier == operation_id:
                return operation
        raise InvalidPlanDefinition(f"Unknown operation: {operation_id!r}.")

    def ids_for(self, definition: PlanDefinition, stage_id: str) -> set[str]:
        return {operation.identifier for operation in definition.operations if operation.stage_id == stage_id}

    def claim(self, run_id: UUID, operation_id: str) -> OperationClaim:
        return OperationClaim(uuid4(), run_id, operation_id)

    def complete(self, claim: OperationClaim, output: dict[str, Any]) -> OperationExecution:
        return OperationExecution(claim.identifier, claim.plan_run_id, claim.operation_id, output)
