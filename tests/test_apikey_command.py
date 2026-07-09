from io import StringIO

import pytest
from django.core.management import call_command

from tokens.models.api_key import ApiKey


@pytest.mark.django_db
def test_apikey_command_generates_infinite_header_key():
    output = StringIO()

    call_command("apikey", stdout=output)

    lines = output.getvalue().splitlines()
    key = next(line.removeprefix("key=") for line in lines if line.startswith("key="))

    api_key = ApiKey.authenticate(key)
    assert api_key is not None
    assert api_key.name == "api key"
    assert "header=apikey" in lines
