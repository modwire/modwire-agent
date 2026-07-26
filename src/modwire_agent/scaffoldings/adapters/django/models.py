import builtins
from uuid import uuid4

from django.db import models


class ShortUuid:
    def __call__(self) -> str:
        return uuid4().hex[:22]


short_uuid = ShortUuid()


class VariableType(models.TextChoices):
    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"


class WriteMode(models.TextChoices):
    MANAGED = "managed", "Managed"
    CREATE_IF_MISSING = "create_if_missing", "Create if missing"


class Scaffolding(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)
    language_id = models.CharField(max_length=64)
    name = models.CharField(max_length=120)
    description = models.TextField()

    Meta = type(
        "Meta",
        (),
        {
            "ordering": ("name",),
            "constraints": [
                models.UniqueConstraint(fields=("language_id", "name"), name="unique_scaffolding_name_per_language")
            ],
        },
    )

    def __str__(self):
        return self.name


class Template(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="templates")
    relative_path = models.CharField(max_length=255)
    file_content = models.TextField(blank=True)
    write_mode = models.CharField(max_length=20, choices=WriteMode.choices, default=WriteMode.MANAGED)

    Meta = type(
        "Meta",
        (),
        {
            "ordering": ("relative_path",),
            "constraints": [
                models.UniqueConstraint(
                    fields=("scaffolding", "relative_path"), name="unique_template_path_per_scaffolding"
                )
            ],
        },
    )

    def __str__(self):
        return self.relative_path


class Variable(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="variables")
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=8, choices=VariableType.choices)
    description = models.CharField(max_length=100)
    default_value = models.JSONField(default=list, blank=True)
    required = models.BooleanField(default=False)

    Meta = builtins.type(
        "Meta",
        (),
        {
            "ordering": ("name",),
            "constraints": [
                models.UniqueConstraint(fields=("scaffolding", "name"), name="unique_variable_name_per_scaffolding")
            ],
        },
    )
