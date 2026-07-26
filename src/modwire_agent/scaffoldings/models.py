from django.db import models

from modwire_agent.shared import SourceCodePackage

from ..core.models import ShortUUIDModel


class Scaffolding(ShortUUIDModel):
    language_id = models.CharField(max_length=32)
    name = models.CharField(max_length=120)
    description = models.TextField()
    spec = models.JSONField(default=dict)

    @property
    def source(self) -> SourceCodePackage:
        return SourceCodePackage.model_validate(self.spec)

    class Meta:
        unique_together = ("language_id", "name")
