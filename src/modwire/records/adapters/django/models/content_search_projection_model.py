from django.db import models
from pgvector.django import VectorField


class ContentSearchProjectionModel(models.Model):
    record = models.OneToOneField("RecordModel", on_delete=models.CASCADE, primary_key=True, related_name="search_projection")
    revision = models.OneToOneField("ContentRevisionModel", on_delete=models.CASCADE, related_name="search_projection")
    embedding = VectorField(dimensions=384, null=True)
    indexed_version = models.PositiveIntegerField()
