from django.contrib import admin

from .models import Scaffolding


@admin.register(Scaffolding)
class ScaffoldingAdmin(admin.ModelAdmin):
    list_display = ("name", "language_id", "description")
    search_fields = ("name", "language_id", "description")
