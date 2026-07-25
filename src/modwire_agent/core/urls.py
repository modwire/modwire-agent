from django.contrib import admin
from django.urls import path
from health_check.views import HealthCheckView

from .api import api
from .siren import facade

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "health/",
        HealthCheckView.as_view(checks=("health_check.checks.Database",)),
    ),
    path("api/", api.urls),
    path("siren/", facade.root),
    path("siren/<path:path>", facade.dispatch),
]
