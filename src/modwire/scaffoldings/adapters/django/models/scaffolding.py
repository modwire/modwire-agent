from django.db import models

from .identifiers import short_uuid


class Scaffolding(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)
    language_id = models.CharField(max_length=64)
    name = models.CharField(max_length=120)
    description = models.TextField()

    Meta = type("Meta", (), {"ordering": ("name",), "constraints": [models.UniqueConstraint(fields=("language_id", "name"), name="unique_scaffolding_name_per_language")]})

    def __str__(self):
        return self.name
