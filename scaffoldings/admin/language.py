from django.contrib import admin

from ..models.language import Language 


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
