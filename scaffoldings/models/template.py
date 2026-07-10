from django.db import models

from .scaffolding import Scaffolding


class Template(models.Model):
    scaffolding = models.ForeignKey(Scaffolding, on_delete=models.CASCADE, related_name="templates")
    relative_path = models.CharField(max_length=255)
    file_content = models.TextField()