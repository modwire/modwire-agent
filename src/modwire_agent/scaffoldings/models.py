from django.db import models
from ..core.models import ShortUUIDModel


class VariableShape(models.TextChoices):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"


class WriteMode(models.TextChoices):
    MANAGED = "managed", "Managed"
    CREATE_IF_MISSING = "create_if_missing", "Create if missing"


class Scaffolding(ShortUUIDModel):
    language_id = models.CharField(max_length=32)
    name = models.CharField(max_length=120)
    description = models.TextField()

    class Meta:
        unique_together = ("language_id", "name",)


class Template(ShortUUIDModel):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="templates")
    relative_path = models.CharField(max_length=255)
    file_content = models.TextField(blank=True)
    write_mode = models.CharField(max_length=20, choices=WriteMode.choices, default=WriteMode.MANAGED)

    class Meta:
        unique_together = ("scaffolding", "relative_path",)


class Variable(ShortUUIDModel):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=120)
    shape = models.CharField(max_length=16, choices=VariableShape.choices)
    description = models.CharField(max_length=100)
    default_value = models.JSONField(default=list, blank=True)
    required = models.BooleanField(default=False)

    class Meta:
        unique_together = ("scaffolding", "name",)
