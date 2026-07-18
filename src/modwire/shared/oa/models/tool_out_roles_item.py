from enum import Enum


class ToolOutRolesItem(str, Enum):
    BUILD = "build"
    COVERAGE = "coverage"
    DEVELOPMENT_RUNNER = "development_runner"
    DIAGRAM_RENDERER = "diagram_renderer"
    DIAGRAM_VALIDATOR = "diagram_validator"
    DOCUMENTATION = "documentation"
    FORMATTER = "formatter"
    LINTER = "linter"
    SECURITY = "security"
    TEST_RUNNER = "test_runner"
    TYPE_CHECKER = "type_checker"

    def __str__(self) -> str:
        return str(self.value)
