from django.contrib import admin

from ..models.variable import Variable 


@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    pass
