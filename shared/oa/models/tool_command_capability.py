from enum import Enum

class ToolCommandCapability(str, Enum):
    AUDIT = "audit"
    BUILD = "build"
    CHECK = "check"
    COVERAGE = "coverage"
    FIX = "fix"
    INIT = "init"
    SERVE = "serve"
    TEST = "test"

    def __str__(self) -> str:
        return str(self.value)
