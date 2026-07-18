from django.db import models
from model_utils.models import TimeStampedModel

from .record import Record


class Content(TimeStampedModel):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="content")
    position = models.PositiveIntegerField()
    content = models.JSONField()
    language = models.CharField(max_length=40)
    metadata = models.JSONField()
