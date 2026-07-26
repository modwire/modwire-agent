from django.db import models
from pgvector.django import VectorField


class RecordModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    tags = models.ManyToManyField("TagModel", related_name="records")


class ContentRevisionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    record = models.ForeignKey(RecordModel, on_delete=models.CASCADE, related_name="content_revisions")
    actor_id = models.CharField(max_length=255, default="legacy")
    actor_kind = models.CharField(max_length=32, default="system")
    markdown = models.TextField()
    schema_version = models.PositiveIntegerField()


class ContentProposalModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    record = models.ForeignKey("RecordModel", on_delete=models.CASCADE, related_name="content_proposals")
    proposed_by_id = models.CharField(max_length=255)
    proposed_by_kind = models.CharField(max_length=32)
    markdown = models.TextField()
    status = models.CharField(max_length=32)


class ContentSearchProjectionModel(models.Model):
    record = models.OneToOneField(
        "RecordModel", on_delete=models.CASCADE, primary_key=True, related_name="search_projection"
    )
    revision = models.OneToOneField("ContentRevisionModel", on_delete=models.CASCADE, related_name="search_projection")
    embedding = VectorField(dimensions=384, null=True)
    indexed_version = models.PositiveIntegerField()


class SectionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    allowed_kinds = models.JSONField(default=list)


class SectionPlacementModel(models.Model):
    section = models.ForeignKey(SectionModel, on_delete=models.CASCADE, related_name="placements")
    record = models.ForeignKey(RecordModel, on_delete=models.CASCADE, related_name="placements")
    position = models.PositiveIntegerField()


class TagModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)


__all__ = [
    "ContentProposalModel",
    "ContentRevisionModel",
    "ContentSearchProjectionModel",
    "RecordModel",
    "SectionModel",
    "SectionPlacementModel",
    "TagModel",
]
