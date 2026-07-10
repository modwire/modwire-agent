from enum import Enum

from django.db import models

from .scaffolding import Scaffolding


class VariableType(Enum):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    YAML = "yaml"


class Variable(models.Model):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=120)
    type = models.TextChoices(max_length=8, choices=VariableType)
    description = models.CharField(max_length=100)
    default_value = models.JSONField(default=list)
