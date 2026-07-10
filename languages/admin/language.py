from django.contrib import admin

from ..models.language import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "executable", "stable_version")
    search_fields = ("name", "executable")
