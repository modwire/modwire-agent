from typing import Any

from ninja import Schema


class GateSatisfactionInput(Schema):
    evidence: dict[str, Any]
