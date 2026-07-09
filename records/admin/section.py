from django.contrib import admin

from ..models.section import Section


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "created", "modified")
    search_fields = ("slug", "title", "description")
    filter_horizontal = ("tags",)
