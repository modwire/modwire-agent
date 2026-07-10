from django.contrib import admin

from ..models.scaffolding import Scaffolding 


@admin.register(Scaffolding)
class ScaffoldingAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
