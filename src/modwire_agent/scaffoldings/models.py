from django.db import models
from model_utils.models import TimeStampedModel


class VariableType(models.TextChoices):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"


class WriteMode(models.TextChoices):
    MANAGED = "managed", "Managed"
    CREATE_IF_MISSING = "create_if_missing", "Create if missing"


class Scaffolding(models.Model):
    language_id = models.CharField(max_length=64)
    name = models.CharField(max_length=120)
    description = models.TextField()


class Template(models.Model):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="templates")
    relative_path = models.CharField(max_length=255)
    file_content = models.TextField(blank=True)
    write_mode = models.CharField(max_length=20, choices=WriteMode.choices, default=WriteMode.MANAGED)


class Variable(models.Model):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=8, choices=VariableType.choices)
    description = models.CharField(max_length=100)
    default_value = models.JSONField(default=list, blank=True)
    required = models.BooleanField(default=False)
