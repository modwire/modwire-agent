from django.db import models

from .identifiers import short_uuid
from .scaffolding import Scaffolding


class Template(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)
    class WriteMode(models.TextChoices):
        MANAGED = "managed", "Managed"
        CREATE_IF_MISSING = "create_if_missing", "Create if missing"

    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="templates")
    relative_path = models.CharField(max_length=255)
    file_content = models.TextField(blank=True)
    write_mode = models.CharField(
        max_length=20,
        choices=WriteMode.choices,
        default=WriteMode.MANAGED,
    )

    class Meta:
        ordering = ("relative_path",)
        constraints = [
            models.UniqueConstraint(
                fields=("scaffolding", "relative_path"),
                name="unique_template_path_per_scaffolding",
            ),
        ]

    def __str__(self):
        return self.relative_path
