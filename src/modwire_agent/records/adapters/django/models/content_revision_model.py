from django.db import models

from .record_model import RecordModel


class ContentRevisionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    record = models.ForeignKey(RecordModel, on_delete=models.CASCADE, related_name="content_revisions")
    actor_id = models.CharField(max_length=255, default="legacy")
    actor_kind = models.CharField(max_length=32, default="system")
    markdown = models.TextField()
    schema_version = models.PositiveIntegerField()
