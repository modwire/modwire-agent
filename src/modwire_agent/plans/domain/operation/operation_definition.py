from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class OperationDefinition:
    identifier: str
    stage_id: str
    extension_key: str
    extension_version: int
    configuration: dict[str, Any]
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    produced_artifact_id: str
    required_artifact_ids: tuple[str, ...]
