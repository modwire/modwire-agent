from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_apikey_command_generates_a_key_that_authenticates_api_requests(client):
    output = StringIO()

    call_command("apikey", stdout=output)

    lines = output.getvalue().splitlines()
    key = next(line.removeprefix("key=") for line in lines if line.startswith("key="))

    assert "header=apikey" in lines
    assert client.get("/api/", HTTP_APIKEY=key).status_code == 200
