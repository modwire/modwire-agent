from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class OperationClaim:
    identifier: UUID
    plan_run_id: UUID
    operation_id: str
