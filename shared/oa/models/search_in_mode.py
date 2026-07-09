from enum import Enum


class SearchInMode(str, Enum):
    FTS = "fts"
    VECTOR = "vector"

    def __str__(self) -> str:
        return str(self.value)
