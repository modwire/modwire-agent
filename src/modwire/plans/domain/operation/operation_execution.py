from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class OperationExecution:
    identifier: UUID
    plan_run_id: UUID
    operation_id: str
    output: dict[str, Any]
