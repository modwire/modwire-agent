from django.db import models

from .identifiers import short_uuid
from .scaffolding import Scaffolding
from .write_mode import WriteMode


class Template(models.Model):
    id = models.CharField(primary_key=True, max_length=22, default=short_uuid, editable=False)

    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="templates")
    relative_path = models.CharField(max_length=255)
    file_content = models.TextField(blank=True)
    write_mode = models.CharField(
        max_length=20,
        choices=WriteMode.choices,
        default=WriteMode.MANAGED,
    )

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
