from django.db import models

from modwire.shared.models import ShortUUIDModel

from .language import Language


class Tool(ShortUUIDModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="tools")
    name = models.CharField(max_length=120)
    roles = models.JSONField(default=list)
    executable = models.CharField(max_length=64)
    package_name = models.CharField(max_length=160)
    stable_version = models.CharField(max_length=32, default="")
    homepage_url = models.URLField()
    config_paths = models.JSONField(default=list)
    default_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ("language", "name")
        constraints = [
            models.UniqueConstraint(fields=("language", "name"), name="unique_tool_name_per_language"),
        ]

    def __str__(self):
        return self.name
