from django.contrib import admin

from ..models.template import Template 


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    pass
