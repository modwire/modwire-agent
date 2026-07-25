from django.db import models


class PlanRunModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    definition = models.ForeignKey("plans.PlanDefinitionModel", on_delete=models.PROTECT, related_name="runs")
    definition_version = models.PositiveIntegerField()
    current_stage_id = models.CharField(max_length=255)
    current_input = models.JSONField(default=dict)
    status = models.CharField(max_length=32)
    revision = models.PositiveIntegerField(default=0)
