from django.db import models


class GateSatisfactionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    plan_run = models.ForeignKey("plans.PlanRunModel", on_delete=models.CASCADE, related_name="gate_satisfactions")
    gate_id = models.CharField(max_length=255)
    satisfaction_key = models.CharField(max_length=300, unique=True)
    evidence = models.JSONField(default=dict)
