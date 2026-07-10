import re

import pytest
from django.core.exceptions import ValidationError
from django.test import Client

from languages.models.language import Language
from languages.models.package_manager import Command, CommandResult, PackageManager
from scaffoldings.models.scaffolding import Scaffolding
from scaffoldings.models.template import Template
from scaffoldings.models.variable import Variable, VariableType
from scaffoldings.services.template import TemplateService
from scaffoldings.services.variable import VariableService
from tokens.models.api_key import ApiKey

SHORT_UUID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{22}$")


@pytest.fixture
def client(db):
    _, key = ApiKey.generate("scaffoldings tests")
    return Client(headers={"apikey": key})


@pytest.fixture
def language(db):
    return Language.objects.create(name="Python", executable="python", stable_version="3.14")


@pytest.fixture
def scaffolding(language):
    return Scaffolding.objects.create(language=language, name="API", description="An API")


@pytest.mark.django_db
def test_all_ecosystem_models_use_short_uuid_ids():
    language = Language.objects.create(name="Python", executable="python", stable_version="3.14")
    manager = PackageManager.objects.create(language=language, name="uv", executable="uv")
    command = Command.objects.create(package_manager=manager, result=CommandResult.INIT, cmd="uv init")
    scaffolding = Scaffolding.objects.create(language=language, name="API", description="An API")
    variable = Variable.objects.create(
        scaffolding=scaffolding,
        name="project_name",
        type=VariableType.STR,
        description="Project name",
        default_value="demo",
    )
    template = Template.objects.create(
        scaffolding=scaffolding,
        relative_path="README.md",
        file_content="# {{ project_name }}",
    )

    ids = {item.id for item in (language, manager, command, scaffolding, variable, template)}
    assert len(ids) == 6
    assert all(SHORT_UUID_PATTERN.fullmatch(item_id) for item_id in ids)


@pytest.mark.django_db
def test_scoped_model_constraints_allow_values_in_different_parents(language):
    other_language = Language.objects.create(name="PHP", executable="php", stable_version="8.5")
    PackageManager.objects.create(language=language, name="composer", executable="composer")
    PackageManager.objects.create(language=other_language, name="composer", executable="composer")
    first = Scaffolding.objects.create(language=language, name="API", description="First")
    second = Scaffolding.objects.create(language=other_language, name="API", description="Second")

    for parent in (first, second):
        Variable.objects.create(
            scaffolding=parent,
            name="name",
            type=VariableType.STR,
            description="Name",
            default_value="demo",
        )
        Template.objects.create(scaffolding=parent, relative_path="README.md", file_content="content")


@pytest.mark.django_db
def test_child_services_validate_duplicates_on_create_and_update(scaffolding, language):
    variables = VariableService()
    templates = TemplateService()
    variable = variables.create(
        scaffolding_id=scaffolding.id,
        name="name",
        type=VariableType.STR,
        description="Name",
        default_value="demo",
    )
    template = templates.create(
        scaffolding_id=scaffolding.id,
        relative_path="README.md",
        file_content="content",
    )

    variables.update(variable.id, name="name")
    templates.update(template.id, relative_path="README.md")

    with pytest.raises(ValidationError):
        variables.create(
            scaffolding_id=scaffolding.id,
            name="name",
            type=VariableType.STR,
            description="Duplicate",
            default_value="demo",
        )
    other = templates.create(scaffolding_id=scaffolding.id, relative_path="other.txt", file_content="other")
    with pytest.raises(ValidationError):
        templates.update(other.id, relative_path="README.md")


@pytest.mark.django_db
def test_languages_and_package_managers_crud_api(client):
    created = client.post(
        "/api/languages",
        data={"name": "Python", "executable": "python", "stable_version": "3.14"},
        content_type="application/json",
    )
    assert created.status_code == 200
    language = created.json()
    assert SHORT_UUID_PATTERN.fullmatch(language["id"])

    manager_response = client.post(
        "/api/package_managers",
        data={"language_id": language["id"], "name": "uv", "executable": "uv"},
        content_type="application/json",
    )
    assert manager_response.status_code == 200
    manager = manager_response.json()

    patched = client.patch(
        f"/api/package_managers/{manager['id']}",
        data={"executable": "uvx"},
        content_type="application/json",
    )
    assert patched.status_code == 200
    assert patched.json()["executable"] == "uvx"
    assert client.get(f"/api/languages/{language['id']}").status_code == 200
    assert client.get("/api/languages").json()[0]["name"] == "Python"


@pytest.mark.django_db
def test_scaffoldings_variables_and_templates_crud_and_duplicate_errors(client, language):
    scaffolding_response = client.post(
        "/api/scaffoldings",
        data={"language_id": language.id, "name": "API", "description": "An API"},
        content_type="application/json",
    )
    assert scaffolding_response.status_code == 200
    scaffolding = scaffolding_response.json()

    variable_data = {
        "scaffolding_id": scaffolding["id"],
        "name": "project_name",
        "type": "str",
        "description": "Project name",
        "default_value": "demo",
    }
    variable_response = client.post("/api/variables", data=variable_data, content_type="application/json")
    assert variable_response.status_code == 200
    assert client.post("/api/variables", data=variable_data, content_type="application/json").status_code == 400

    template_data = {
        "scaffolding_id": scaffolding["id"],
        "relative_path": "README.md",
        "file_content": "# Project",
    }
    template_response = client.post("/api/templates", data=template_data, content_type="application/json")
    assert template_response.status_code == 200
    template = template_response.json()
    assert client.post("/api/templates", data=template_data, content_type="application/json").status_code == 400

    assert client.patch(
        f"/api/templates/{template['id']}",
        data={"file_content": "updated"},
        content_type="application/json",
    ).json()["file_content"] == "updated"
    assert client.delete(f"/api/templates/{template['id']}").status_code == 204
    assert client.get("/api/scaffoldings/not-found").status_code == 404
