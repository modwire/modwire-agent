import pytest
from django.core.exceptions import ValidationError
from django.test import Client

from languages.models.language import Language
from scaffoldings.models.scaffolding import Scaffolding
from scaffoldings.models.template import Template
from scaffoldings.models.variable import Variable, VariableType
from tokens.models.api_key import ApiKey


@pytest.fixture
def client(db):
    _, key = ApiKey.generate("scaffolding preview tests")
    return Client(headers={"apikey": key})


@pytest.fixture
def preview_scaffolding(db):
    language = Language.objects.create(name="Python", executable="python", stable_version="3.14")
    scaffolding = Scaffolding.objects.create(language=language, name="Service", description="A service")
    Variable.objects.create(
        scaffolding=scaffolding,
        name="project_name",
        type=VariableType.STR,
        description="Project name",
        default_value="demo project",
    )
    Variable.objects.create(
        scaffolding=scaffolding,
        name="modules",
        type=VariableType.LIST,
        description="Modules",
        default_value=[],
        required=True,
    )
    first = Template.objects.create(
        scaffolding=scaffolding,
        relative_path="{{ project_name | snake }}/main.py",
        file_content="class {{ project_name | pascal }}:\n    pass\n",
    )
    Template.objects.create(
        scaffolding=scaffolding,
        relative_path="{{ project_name | kebab }}/README.md",
        file_content="# {{ project_name | title }}\n",
    )
    return scaffolding, first


@pytest.mark.django_db
def test_variable_default_must_match_type(preview_scaffolding):
    scaffolding, _ = preview_scaffolding
    variable = Variable(
        scaffolding=scaffolding,
        name="bad",
        type=VariableType.DICT,
        description="Bad",
        default_value=[],
    )
    with pytest.raises(ValidationError):
        variable.full_clean()


def test_schema_endpoint(client, preview_scaffolding):
    scaffolding, _ = preview_scaffolding
    response = client.get(f"/api/scaffoldings/{scaffolding.id}/schema")
    assert response.status_code == 200
    schema = response.json()["properties"]
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["additionalProperties"] is False
    assert schema["properties"]["modules"]["type"] == "array"
    assert schema["required"] == ["modules"]


def test_preview_renders_complete_package_and_unsaved_override(client, preview_scaffolding):
    scaffolding, first = preview_scaffolding
    response = client.post(
        f"/api/scaffoldings/{scaffolding.id}/preview",
        data={
            "values": {"project_name": "HTTP API", "modules": ["users"]},
            "template_overrides": [
                {
                    "template_id": str(first.id),
                    "relative_path": first.relative_path,
                    "file_content": "def {{ project_name | camel }}():\n    pass\n",
                }
            ],
        },
        content_type="application/json",
    )
    assert response.status_code == 200, response.content
    files = response.json()["properties"]["files"]
    assert [item["path"] for item in files] == ["http-api/README.md", "http_api/main.py"]
    assert "def httpApi()" in files[1]["source"]
    assert "<span" in files[1]["html"]
    first.refresh_from_db()
    assert first.file_content.startswith("class")


def test_preview_returns_structured_errors(client, preview_scaffolding):
    scaffolding, first = preview_scaffolding
    missing = client.post(
        f"/api/scaffoldings/{scaffolding.id}/preview",
        data={"values": {}},
        content_type="application/json",
    )
    assert missing.status_code == 422
    assert missing.json()["detail"]["errors"][0]["code"] == "required_variable"

    unsafe = client.post(
        f"/api/scaffoldings/{scaffolding.id}/preview",
        data={
            "values": {"modules": []},
            "template_overrides": [
                {
                    "template_id": str(first.id),
                    "relative_path": first.relative_path,
                    "file_content": "{{ ''.__class__ }}",
                }
            ],
        },
        content_type="application/json",
    )
    assert unsafe.status_code == 422
    assert unsafe.json()["detail"]["errors"][0]["code"] == "jinja_render"
