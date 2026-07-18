from enum import Enum


class ToolRole(str, Enum):
    BUILD = "build"
    COVERAGE = "coverage"
    DEVELOPMENT_RUNNER = "development_runner"
    DOCUMENTATION = "documentation"
    FORMATTER = "formatter"
    LINTER = "linter"
    SECURITY = "security"
    TEST_RUNNER = "test_runner"
    TYPE_CHECKER = "type_checker"

    def __str__(self) -> str:
        return str(self.value)
