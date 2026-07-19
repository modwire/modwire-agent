from django.db import models

from .record_model import RecordModel
from .section_model import SectionModel


class SectionPlacementModel(models.Model):
    section = models.ForeignKey(SectionModel, on_delete=models.CASCADE, related_name="placements")
    record = models.ForeignKey(RecordModel, on_delete=models.CASCADE, related_name="placements")
    position = models.PositiveIntegerField()
