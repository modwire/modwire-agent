from django.db import models

from .language import Language
from .package_manager import PackageManager


class Scaffolding(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    package_manager = models.ForeignKey(PackageManager, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120)


    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name
