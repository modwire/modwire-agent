import hashlib
import secrets

from django.db import models
from django.utils import timezone


class ApiKey(models.Model):
    name = models.CharField(max_length=120)
    prefix = models.CharField(max_length=12, unique=True, editable=False)
    key_hash = models.CharField(max_length=64, unique=True, editable=False)
    last_used_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name

    @classmethod
    def generate(cls, name: str) -> tuple["ApiKey", str]:
        key = secrets.token_urlsafe(48)
        return cls.objects.create(name=name, prefix=key[:12], key_hash=cls.hash_key(key)), key

    @classmethod
    def hash_key(cls, key: str) -> str:
        return hashlib.sha256(key.encode("utf-8")).hexdigest()

    @classmethod
    def authenticate(cls, key: str | None) -> "ApiKey | None":
        if not key:
            return None

        api_key = cls.objects.filter(key_hash=cls.hash_key(key), is_active=True).first()
        if api_key is None:
            return None

        api_key.last_used_at = timezone.now()
        api_key.save(update_fields=["last_used_at", "updated_at"])
        return api_key
