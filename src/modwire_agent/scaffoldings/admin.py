from django.contrib import admin

from .models import Scaffolding, Template, Variable


@admin.register(Scaffolding)
class ScaffoldingAdmin(admin.ModelAdmin): ...


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "relative_path", "scaffolding")
    list_filter = ("scaffolding",)
    search_fields = ("relative_path",)


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "scaffolding", "type")
    list_filter = ("type", "scaffolding")
    search_fields = ("name",)
