from django.db import models


class OperationExecutionModel(models.Model):
    identifier = models.UUIDField(primary_key=True)
    plan_run = models.ForeignKey("plans.PlanRunModel", on_delete=models.CASCADE, related_name="operation_executions")
    operation_id = models.CharField(max_length=255)
    execution_key = models.CharField(max_length=300, unique=True)
    status = models.CharField(max_length=32, default="complete")
    output = models.JSONField(default=dict)
