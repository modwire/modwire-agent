from django.db import models


class PlanArtifactModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    plan_run = models.ForeignKey("plans.PlanRunModel", on_delete=models.CASCADE, related_name="artifacts")
    artifact_id = models.CharField(max_length=255)
    artifact_key = models.CharField(max_length=300, unique=True)
    payload = models.JSONField(default=dict)
