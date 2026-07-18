from django.core.exceptions import ValidationError
from django.db import models

from modwire.shared.models import ShortUUIDModel

from .scaffolding import Scaffolding


class VariableType(models.TextChoices):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"


class Variable(ShortUUIDModel):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=8, choices=VariableType.choices)
    description = models.CharField(max_length=100)
    default_value = models.JSONField(default=list, blank=True)
    required = models.BooleanField(default=False)

    def clean(self):
        super().clean()
        expected = {
            VariableType.STR: str,
            VariableType.INT: int,
            VariableType.FLOAT: float,
            VariableType.BOOL: bool,
            VariableType.LIST: list,
            VariableType.DICT: dict,
        }.get(self.type)
        value = self.default_value
        valid = expected is not None and type(value) is expected
        if self.type == VariableType.FLOAT:
            valid = type(value) in {int, float}
        if not valid:
            raise ValidationError({"default_value": f"Default value must match variable type '{self.type}'."})

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
