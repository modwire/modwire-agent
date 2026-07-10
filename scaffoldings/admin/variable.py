from django.contrib import admin

from ..models.variable import Variable


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "scaffolding", "type")
    list_filter = ("type", "scaffolding")
    search_fields = ("name",)
