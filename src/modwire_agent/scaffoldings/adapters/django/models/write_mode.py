from django.db import models


class WriteMode(models.TextChoices):
    MANAGED = "managed", "Managed"
    CREATE_IF_MISSING = "create_if_missing", "Create if missing"
