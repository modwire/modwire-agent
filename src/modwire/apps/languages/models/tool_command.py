from django.db import models

from modwire.shared.models import ShortUUIDModel

from .tool import Tool


class ToolCommandCapability(models.TextChoices):
    INIT = "init"
    CHECK = "check"
    FIX = "fix"
    TEST = "test"
    COVERAGE = "coverage"
    BUILD = "build"
    SERVE = "serve"
    AUDIT = "audit"


class ToolCommand(ShortUUIDModel):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name="commands")
    capability = models.CharField(max_length=32, choices=ToolCommandCapability.choices)
    cmd = models.CharField(max_length=255)

    class Meta:
        ordering = ("tool", "capability")
        constraints = [
            models.UniqueConstraint(fields=("tool", "capability"), name="unique_command_capability_per_tool"),
        ]

    def __str__(self):
        return self.cmd
