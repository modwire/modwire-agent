from django.contrib import admin

from ..models.package_manager import Command, PackageManager


@admin.register(PackageManager)
class PackageManagerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "language", "executable")
    list_filter = ("language",)
    search_fields = ("name", "executable")


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("id", "package_manager", "result", "cmd")
    list_filter = ("result", "package_manager")
