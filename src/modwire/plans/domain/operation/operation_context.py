from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class OperationContext:
    plan_run_id: UUID
    operation_id: str
    stage_input: dict[str, Any]
    artifacts: dict[str, dict[str, Any]]
    configuration: dict[str, Any]
