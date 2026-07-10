from django.contrib import admin
from django.urls import path
from health_check.views import HealthCheckView

from .api import api
from .browser import api_root, browser

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view()),
    path("api/", api_root, name="api-root"),
    path("api/", api.urls),
    path("browser/", browser, name="api-browser"),
    path("browser/<path:path>", browser, name="api-browser-assets"),
]
