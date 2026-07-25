from django.db import models


class TagModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
