from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ...use_cases.gate.satisfy_stage_gate import SatisfyStageGate
from .schemas.gate_satisfaction_input import GateSatisfactionInput


@api_controller("/plans/runs", tags=["plans"])
class SatisfyStageGateController(ControllerBase):
    @route.post("/{run_id}/gates/{gate_id}/satisfactions", response={204: None}, operation_id="satisfy_stage_gate")
    def satisfy(self, request: Any, run_id: UUID, gate_id: str, payload: GateSatisfactionInput) -> int:
        DjangoRequest.resolve(request, SatisfyStageGate).execute(run_id, gate_id, payload.evidence)
        return 204
