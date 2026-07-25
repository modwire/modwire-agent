from django.db import models


class PlanDefinitionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    version = models.PositiveIntegerField()
    publication_key = models.CharField(max_length=300, unique=True)
    start_stage_id = models.CharField(max_length=255)
    stages = models.JSONField(default=list)
    transitions = models.JSONField(default=list)
    gates = models.JSONField(default=list)
    operations = models.JSONField(default=list)
    artifacts = models.JSONField(default=list)
