from django.conf import settings
from django.test import RequestFactory, override_settings

from core.api import api
from shared.api.siren import api_root_document


def test_api_and_discovery_document_report_the_release_version():
    request = RequestFactory().get("/api/", HTTP_HOST="localhost")

    assert api.version == settings.RELEASE_VERSION
    assert api.get_openapi_schema()["info"]["version"] == settings.RELEASE_VERSION
    assert api_root_document(request)["properties"]["version"] == settings.RELEASE_VERSION


@override_settings(ALLOWED_HOSTS=["modwire.example"])
def test_discovery_links_honor_https_forwarded_by_the_deployment_proxy():
    request = RequestFactory().get(
        "/api/",
        HTTP_HOST="modwire.example",
        HTTP_X_FORWARDED_PROTO="https",
    )

    links = api_root_document(request)["links"]

    assert all(link["href"].startswith("https://modwire.example/") for link in links)
