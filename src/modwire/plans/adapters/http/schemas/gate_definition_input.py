from typing import Any

from ninja import Schema


class GateDefinitionInput(Schema):
    id: str
    stage_id: str
    evidence_schema: dict[str, Any]
