from django.contrib import admin

from ..models.command import Command


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("id", "package_manager", "result", "cmd")
    list_filter = ("result", "package_manager")
