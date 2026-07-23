from django.contrib import admin
from django.urls import path
from health_check.views import HealthCheckView
from modwire_hex.django import DjangoNinja

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "health/",
        HealthCheckView.as_view(checks=("health_check.checks.Database",)),
    ),
    path("api/", DjangoNinja.api().urls),
]
