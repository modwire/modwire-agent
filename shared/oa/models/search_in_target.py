from enum import Enum


class SearchInTarget(str, Enum):
    ALL = "all"
    RECORDS = "records"
    SECTIONS = "sections"

    def __str__(self) -> str:
        return str(self.value)
