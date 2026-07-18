from django.contrib import admin

from ..models.package_manager import PackageManager


@admin.register(PackageManager)
class PackageManagerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "language", "executable")
    list_filter = ("language",)
    search_fields = ("name", "executable")
