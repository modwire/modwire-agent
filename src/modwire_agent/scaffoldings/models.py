from django.db import models

from ..core.models import ShortUUIDModel


class Scaffolding(ShortUUIDModel):
    language_id = models.CharField(max_length=32)
    name = models.CharField(max_length=120)
    description = models.TextField()
    spec = models.JSONField(default=dict)

    class Meta:
        unique_together = ("language_id", "name")
