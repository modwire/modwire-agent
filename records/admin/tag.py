from django.contrib import admin

from ..models.tag import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "description", "created", "modified")
    search_fields = ("slug", "name", "description")
