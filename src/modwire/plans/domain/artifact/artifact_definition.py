from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ArtifactDefinition:
    identifier: str
    producer_operation_id: str
    schema: dict[str, Any]
