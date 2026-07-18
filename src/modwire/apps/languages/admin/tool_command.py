from django.contrib import admin

from ..models.tool_command import ToolCommand


@admin.register(ToolCommand)
class ToolCommandAdmin(admin.ModelAdmin):
    list_display = ("id", "tool", "capability", "cmd")
    list_filter = ("capability", "tool")
