from enum import Enum


class ConvergencePlanOutScaffolding(str, Enum):
    CREATE = "create"
    UNCHANGED = "unchanged"
    UPDATE = "update"

    def __str__(self) -> str:
        return str(self.value)
