from enum import StrEnum


class RecordKind(StrEnum):
    RULE = "rule"
    DECISION = "decision"
    GUIDE = "guide"
    REFERENCE = "reference"
