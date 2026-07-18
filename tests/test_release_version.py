from io import StringIO

import pytest
from django.conf import settings
from django.core.management import call_command
from django.test import override_settings


def api_key() -> str:
    output = StringIO()
    call_command("apikey", stdout=output)
    return next(line.removeprefix("key=") for line in output.getvalue().splitlines() if line.startswith("key="))


@pytest.mark.django_db
def test_api_and_discovery_document_report_the_release_version(client):
    key = api_key()
    discovery = client.get("/api/", HTTP_APIKEY=key)
    openapi = client.get("/api/openapi.json", HTTP_APIKEY=key)

    assert discovery.json()["properties"]["version"] == settings.RELEASE_VERSION
    assert openapi.json()["info"]["version"] == settings.RELEASE_VERSION


@pytest.mark.django_db
@override_settings(ALLOWED_HOSTS=["modwire.example"])
def test_discovery_links_honor_https_forwarded_by_the_deployment_proxy(client):
    response = client.get(
        "/api/",
        HTTP_HOST="modwire.example",
        HTTP_X_FORWARDED_PROTO="https",
        HTTP_APIKEY=api_key(),
    )

    links = response.json()["links"]

    assert all(link["href"].startswith("https://modwire.example/") for link in links)
