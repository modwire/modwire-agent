from django.db import models


class RecordModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    kind = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    tags = models.ManyToManyField("TagModel", related_name="records")
