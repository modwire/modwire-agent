from django.conf import settings
from django.test import RequestFactory

from core.api import api
from shared.api.siren import api_root_document


def test_api_and_discovery_document_report_the_release_version():
    request = RequestFactory().get("/api/", HTTP_HOST="localhost")

    assert api.version == settings.RELEASE_VERSION
    assert api.get_openapi_schema()["info"]["version"] == settings.RELEASE_VERSION
    assert api_root_document(request)["properties"]["version"] == settings.RELEASE_VERSION
