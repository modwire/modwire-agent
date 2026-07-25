from typing import Any

from ninja import Schema


class StageDefinitionInput(Schema):
    id: str
    input_schema: dict[str, Any]
    submission_schema: dict[str, Any]
