from django.contrib import admin
from django.urls import path
from health_check.views import HealthCheckView

from modwire_agent.browser.adapters.http.views import BrowserIndexView

from .api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "health/",
        HealthCheckView.as_view(checks=("health_check.checks.Database",)),
    ),
    path("api/", api.urls),
    path("", BrowserIndexView.as_view()),
]
