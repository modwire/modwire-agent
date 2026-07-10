from django.contrib import admin

from ..models.language import Language 


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass
