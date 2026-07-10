from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=120)
    executable = models.CharField(max_length=32)
    stable_version = models.CharField(max_length=16)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name
