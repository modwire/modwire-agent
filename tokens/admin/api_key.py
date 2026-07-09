from django.contrib import admin

from ..models.api_key import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "prefix", "is_active", "last_used_at", "created_at")
    list_filter = ("is_active",)
    readonly_fields = ("prefix", "key_hash", "last_used_at", "created_at", "updated_at")
    search_fields = ("name", "prefix")
