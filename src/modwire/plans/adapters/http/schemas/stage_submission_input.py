from typing import Any

from ninja import Schema


class StageSubmissionInput(Schema):
    payload: dict[str, Any]
