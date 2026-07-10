from django.db import models

from ...languages.models.language import Language


class Scaffolding(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()

    class Meta:
        unique_together = ("language", "slug",)