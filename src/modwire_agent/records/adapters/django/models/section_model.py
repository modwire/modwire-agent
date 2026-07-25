from django.db import models


class SectionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    allowed_kinds = models.JSONField(default=list)
