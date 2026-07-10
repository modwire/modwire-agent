from django.db import models

from shared.models import ShortUUIDModel

from .scaffolding import Scaffolding


class VariableType(models.TextChoices):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    YAML = "yaml"


class Variable(ShortUUIDModel):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=8, choices=VariableType.choices)
    description = models.CharField(max_length=100)
    default_value = models.JSONField(default=list)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=("scaffolding", "name"),
                name="unique_variable_name_per_scaffolding",
            ),
        ]

    def __str__(self):
        return self.name
