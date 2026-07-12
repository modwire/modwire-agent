from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

from .record import Record


class ContentRole(models.TextChoices):
    HEADING = "heading", "Heading"
    SUBHEADING = "subheading", "Subheading"
    PARAGRAPH = "paragraph", "Paragraph"
    LIST = "list", "List"
    MARKDOWN = "markdown", "Markdown"
    SNIPPET = "snippet", "Snippet"
    IMAGE = "image", "Image"


class Content(TimeStampedModel):
    Role = ContentRole

    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="content")
    position = models.PositiveIntegerField()
    role = models.CharField(max_length=20, choices=Role.choices)
    content = models.JSONField()
    language = models.CharField(max_length=40)
    metadata = models.JSONField()

    class Meta:
        ordering = ["record_id", "position", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["record", "position"],
                name="unique_record_content_position",
            ),
        ]

    def __str__(self):
        return f"{self.record_id}#{self.position}:{self.role}"

    def clean(self):
        super().clean()
        if self.role == self.Role.LIST:
            if not isinstance(self.content, list) or not all(
                isinstance(item, str) for item in self.content
            ):
                raise ValidationError({"content": "List content must be an array of strings."})
        elif not isinstance(self.content, str):
            raise ValidationError({"content": "Non-list content must be a string."})
        if self.role == self.Role.SNIPPET and not self.language:
            raise ValidationError({"language": "Snippet content requires a language."})
        if not self.language:
            raise ValidationError({"language": "Content language is required."})
        if not isinstance(self.metadata, dict):
            raise ValidationError({"metadata": "Content metadata must be an object."})
