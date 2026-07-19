from typing import Any

from ninja import Schema


class PlanRunInput(Schema):
    definition_id: str
    initial_input: dict[str, Any]
