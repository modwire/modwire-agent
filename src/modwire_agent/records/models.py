from django.db import models
from pgvector.django import VectorField


class Record(models.Model):
    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    tags = models.ManyToManyField("TagModel", related_name="records")


class ContentRevision(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="content_revisions")
    actor_id = models.CharField(max_length=255, default="legacy")
    actor_kind = models.CharField(max_length=32, default="system")
    markdown = models.TextField()
    schema_version = models.PositiveIntegerField()


class ContentProposal(models.Model):
    record = models.ForeignKey("RecordModel", on_delete=models.CASCADE, related_name="content_proposals")
    proposed_by_id = models.CharField(max_length=255)
    proposed_by_kind = models.CharField(max_length=32)
    markdown = models.TextField()
    status = models.CharField(max_length=32)


class ContentSearchProjection(models.Model):
    record = models.OneToOneField( "RecordModel", on_delete=models.CASCADE, related_name="search_projection")
    revision = models.OneToOneField("ContentRevisionModel", on_delete=models.CASCADE, related_name="search_projection")
    embedding = VectorField(dimensions=384, null=True)
    indexed_version = models.PositiveIntegerField()


class Section(models.Model):
    title = models.CharField(max_length=255)
    allowed_kinds = models.JSONField(default=list)


class SectionPlacement(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="placements")
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="placements")
    position = models.PositiveIntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
