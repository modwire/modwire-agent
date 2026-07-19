from django.db import models

from .identifiers import short_uuid
from .scaffolding import Scaffolding


class VariableType(models.TextChoices):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"


class Variable(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=8, choices=VariableType.choices)
    description = models.CharField(max_length=100)
    default_value = models.JSONField(default=list, blank=True)
    required = models.BooleanField(default=False)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("scaffolding", "name"),
                name="unique_variable_name_per_scaffolding",
            ),
        ]
