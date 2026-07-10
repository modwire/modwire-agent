from django.db import models

from languages.models.language import Language
from shared.models import ShortUUIDModel


class Scaffolding(ShortUUIDModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="scaffoldings")
    name = models.CharField(max_length=120)
    description = models.TextField()

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("language", "name"),
                name="unique_scaffolding_name_per_language",
            ),
        ]

    def __str__(self):
        return self.name
