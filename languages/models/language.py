from django.db import models

from shared.models import ShortUUIDModel


class Language(ShortUUIDModel):
    name = models.CharField(max_length=120, unique=True)
    executable = models.CharField(max_length=32)
    stable_version = models.CharField(max_length=16)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
