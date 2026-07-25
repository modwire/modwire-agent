from django.db import models


class StageSubmissionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    plan_run = models.ForeignKey("plans.PlanRunModel", on_delete=models.CASCADE, related_name="submissions")
    stage_id = models.CharField(max_length=255)
    payload = models.JSONField(default=dict)
