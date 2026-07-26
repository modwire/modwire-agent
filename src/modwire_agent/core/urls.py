from django.contrib import admin
from django.urls import path
from health_check.views import HealthCheckView

from modwire_agent.browser.adapters.http.controllers import BrowserIndexView

from .api import api
from .siren import facade

urlpatterns = [
    path("", BrowserIndexView.as_view(), name="browser-index"),
    path("admin/", admin.site.urls),
    path(
        "health/",
        HealthCheckView.as_view(checks=("health_check.checks.Database",)),
    ),
    path("api/", api.urls),
    path("siren/", facade.root),
    path("siren/<path:path>", facade.dispatch),
]
