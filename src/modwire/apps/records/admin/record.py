from django.contrib import admin

from ..models.record import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "section", "created", "modified")
    list_filter = ("section", "tags")
    search_fields = ("slug", "local_slug", "title", "description", "search_text")
    filter_horizontal = ("tags",)
