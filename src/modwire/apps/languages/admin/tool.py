from django.contrib import admin

from ..models.tool import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "language", "executable", "default_enabled")
    list_filter = ("language", "default_enabled")
    search_fields = ("name", "package_name")
