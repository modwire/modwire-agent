from django.db import models

from .language import Language


class PackageManager(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, auto_created=True)
    executable = models.CharField(max_length=32)
    dependencies = models.JSONField(default=list)
    dev_dependencies = models.JSONField(default=list)
    scripts = models.JSONField(default=dict)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
