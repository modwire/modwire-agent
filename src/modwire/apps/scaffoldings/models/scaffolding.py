from django.db import models

from modwire.shared.models import ShortUUIDModel


class Scaffolding(ShortUUIDModel):
    language_id = models.CharField(max_length=64)
    name = models.CharField(max_length=120)
    description = models.TextField()

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("language_id", "name"),
                name="unique_scaffolding_name_per_language",
            ),
        ]

    def __str__(self):
        return self.name
