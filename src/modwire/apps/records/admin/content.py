from django.contrib import admin

from ..models.content import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("record", "position", "role", "language", "created", "modified")
    list_filter = ("role", "language")
    search_fields = ("record__slug", "content", "language")
