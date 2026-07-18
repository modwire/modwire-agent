from django.db import models
from model_utils.models import TimeStampedModel
from pgvector.django import VectorField

EMBEDDING_DIMENSIONS = 384


class Section(TimeStampedModel):
    slug = models.SlugField(primary_key=True, max_length=80, validators=[slug_validator])
    title = models.CharField(max_length=160)
    description = models.TextField()
    search_text = models.TextField()
    embedding = VectorField(dimensions=EMBEDDING_DIMENSIONS)

    class Meta:
        ordering = ["slug"]
