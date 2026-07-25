from django.apps import AppConfig


class PlansConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modwire_agent.plans.adapters.django"
    label = "plans"
