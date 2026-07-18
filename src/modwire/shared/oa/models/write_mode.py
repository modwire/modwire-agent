from enum import Enum


class WriteMode(str, Enum):
    CREATE_IF_MISSING = "create_if_missing"
    MANAGED = "managed"

    def __str__(self) -> str:
        return str(self.value)
