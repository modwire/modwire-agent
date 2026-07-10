from django.db import models

from shared.models import ShortUUIDModel

from .language import Language


class PackageManager(ShortUUIDModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="package_managers")
    name = models.CharField(max_length=120)
    executable = models.CharField(max_length=32)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("language", "name"),
                name="unique_package_manager_name_per_language",
            ),
        ]

    def __str__(self):
        return self.name
