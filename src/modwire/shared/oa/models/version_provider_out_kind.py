from enum import Enum


class VersionProviderOutKind(str, Enum):
    ENDOFLIFE = "endoflife"
    NPM = "npm"

    def __str__(self) -> str:
        return str(self.value)
