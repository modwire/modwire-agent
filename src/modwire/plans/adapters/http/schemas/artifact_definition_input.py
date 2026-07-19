from typing import Any

from ninja import Schema


class ArtifactDefinitionInput(Schema):
    id: str
    producer_operation_id: str
    output_schema: dict[str, Any]
