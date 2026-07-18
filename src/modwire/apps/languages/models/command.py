from django.db import models

from modwire.shared.models import ShortUUIDModel

from .package_manager import PackageManager


class CommandResult(models.TextChoices):
    INIT = "init"
    INSTALL = "install"
    ADD_RUNTIME = "add_runtime"
    ADD_DEVELOPMENT = "add_development"
    ADD_OPTIONAL = "add_optional"
    ADD_PEER = "add_peer"
    REMOVE = "remove"
    UPDATE = "update"
    LOCK = "lock"
    RUN = "run"
    PUBLISH = "publish"
    AUDIT = "audit"


class Command(ShortUUIDModel):
    package_manager = models.ForeignKey(PackageManager, on_delete=models.CASCADE, related_name="commands")
    result = models.CharField(max_length=32, choices=CommandResult.choices)
    cmd = models.CharField(max_length=255)

    class Meta:
        ordering = ("package_manager", "result")
        constraints = [
            models.UniqueConstraint(
                fields=("package_manager", "result"),
                name="unique_command_result_per_package_manager",
            ),
        ]

    def __str__(self):
        return self.cmd
