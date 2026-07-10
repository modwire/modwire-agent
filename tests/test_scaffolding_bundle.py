import pytest
from django.test import Client

from languages.models.language import Language
from scaffoldings.models.scaffolding import Scaffolding
from scaffoldings.models.template import Template
from scaffoldings.models.variable import Variable
from scaffoldings.services.bundle import ScaffoldingBundleService
from scaffoldings.services.scaffolding import ScaffoldingService
from tokens.models.api_key import ApiKey


@pytest.mark.django_db
def test_bundle_service_returns_ordered_generic_scaffolding_data():
    language = Language.objects.create(name="TypeScript", executable="node", stable_version="5.8")
    scaffolding = Scaffolding.objects.create(language=language, name="React", description="React app")
    Variable.objects.create(
        scaffolding=scaffolding,
        name="project_title",
        type="str",
        description="Title",
        default_value="App",
    )
    Template.objects.create(scaffolding=scaffolding, relative_path="src/main.tsx", file_content="{{ project_title }}")

    bundle = ScaffoldingBundleService(ScaffoldingService()).get(scaffolding.id)

    assert bundle == scaffolding


@pytest.mark.django_db
def test_bundle_endpoint_uses_schema_to_project_related_models():
    language = Language.objects.create(name="TypeScript", executable="node", stable_version="5.8")
    scaffolding = Scaffolding.objects.create(language=language, name="React", description="React app")
    Variable.objects.create(
        scaffolding=scaffolding,
        name="title",
        type="str",
        description="Title",
        default_value="App",
    )
    Template.objects.create(scaffolding=scaffolding, relative_path="index.html", file_content="{{ title }}")
    _, key = ApiKey.generate("bundle-test")

    response = Client(headers={"apikey": key}).get(f"/api/scaffoldings/{scaffolding.id}/bundle")

    assert response.status_code == 200
    properties = response.json()["properties"]
    assert properties["variables"][0]["name"] == "title"
    assert properties["templates"][0]["relative_path"] == "index.html"
