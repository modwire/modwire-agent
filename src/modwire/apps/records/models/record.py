from django.db import models
from model_utils.models import TimeStampedModel
from pgvector.django import VectorField

from .section import EMBEDDING_DIMENSIONS, Section


class Record(TimeStampedModel):
    slug = models.CharField(primary_key=True, max_length=180)
    local_slug = models.SlugField(max_length=80, validators=[slug_validator])
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name="records")
    title = models.CharField(max_length=160)
    description = models.TextField()
    sources = models.JSONField()
    search_text = models.TextField()
    embedding = VectorField(dimensions=EMBEDDING_DIMENSIONS)
