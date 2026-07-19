from django.contrib import admin

from ..models.template import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "relative_path", "scaffolding")
    list_filter = ("scaffolding",)
    search_fields = ("relative_path",)
