from enum import Enum

from django.db import models

from .language import Language


class PackageManager(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="package_managers")
    name = models.CharField(max_length=120)
    executable = models.CharField(max_length=32)

    class Meta:
        ordering = ("name",)


class CommandResult(Enum):
    INIT = "init"
    INSTALL = "install"
    ADD = "add"
    REMOVE = "remove"


class Command(models.Model):
    package_manager = models.ForeignKey(PackageManager, on_delete=models.CASCADE)
    result = models.TextChoices(max_length=16, choices=CommandResult)
    cmd = models.CharField(max_length=255)
