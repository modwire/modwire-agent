from django.contrib import admin

from ..models.package_manager import PackageManager 


@admin.register(PackageManager)
class PackageManagerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
