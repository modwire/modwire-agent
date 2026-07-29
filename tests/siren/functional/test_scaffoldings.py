import pytest
from django.test import Client

from modwire_agent.core.api import api
from modwire_agent.core.siren import facade

SIREN_MEDIA_TYPE = "application/vnd.siren+json"


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def scaffolding_payload() -> dict[str, object]:
    return {
        "language_id": "python",
        "name": "Package",
        "description": "Creates a Python package.",
        "spec": {
            "language": "python",
            "package": {"files": {"src/package/__init__.py": ""}},
        },
    }


def test_siren_operation_catalog_matches_openapi() -> None:
    schema = api.get_openapi_schema()
    openapi_operation_ids = {
        operation["operationId"]
        for path_item in schema["paths"].values()
        for operation in path_item.values()
        if isinstance(operation, dict) and isinstance(operation.get("operationId"), str)
    }

    assert {operation.name for operation in facade.engine.api.operations} == openapi_operation_ids
    rendering = schema["paths"]["/api/scaffoldings/{scaffolding_id}/renderings"]["post"]
    assert rendering["operationId"] == "render_scaffolding"


@pytest.mark.django_db
def test_siren_discovers_and_creates_scaffoldings(
    client: Client,
    scaffolding_payload: dict[str, object],
) -> None:
    root = client.get("/siren/")

    assert root.status_code == 200
    assert root["Content-Type"] == SIREN_MEDIA_TYPE
    assert root.json()["class"] == ["api", "entry-point"]
    assert {link["href"] for link in root.json()["links"]} >= {"http://testserver/siren/scaffoldings"}

    collection = client.get("/siren/scaffoldings")

    assert collection.status_code == 200
    assert collection["Content-Type"] == SIREN_MEDIA_TYPE
    assert collection.json()["class"] == ["collection", "scaffolding"]
    action = next(action for action in collection.json()["actions"] if action["name"] == "create_scaffolding")
    assert action["href"] == "http://testserver/siren/scaffoldings"
    assert action["method"] == "POST"
    assert [field["name"] for field in action["fields"]] == ["language_id", "name", "description", "spec"]
    assert action["x-form"]["schema"]["required"] == ["language_id", "name", "description", "spec"]

    created = client.post(
        action["href"].removeprefix("http://testserver"),
        data=scaffolding_payload,
        content_type="application/json",
    )

    assert created.status_code == 201
    assert created["Content-Type"] == SIREN_MEDIA_TYPE
    assert created.json()["class"] == ["scaffolding"]
    assert created.json()["properties"]["name"] == "Package"

    details = client.get(f"/siren/scaffoldings/{created.json()['properties']['id']}")

    assert details.status_code == 200
    assert details["Content-Type"] == SIREN_MEDIA_TYPE
    assert details.json()["class"] == ["scaffolding"]
    assert {action["name"] for action in details.json()["actions"]} == {
        "delete_scaffolding",
        "get_scaffolding",
        "update_scaffolding",
    }

    rendering = client.post(
        f"/siren/scaffoldings/{created.json()['properties']['id']}/renderings",
        data={"parameters": {}},
        content_type="application/json",
    )

    assert rendering.status_code == 200
    assert rendering["Content-Type"] == SIREN_MEDIA_TYPE
    assert rendering.json()["class"] == ["collection", "rendering"]
    assert rendering.json()["entities"][0]["properties"] == {"files": {"src/package/__init__.py": ""}}


def test_siren_projects_commands(client: Client) -> None:
    response = client.get("/siren/openapi.json")

    assert response.status_code == 200
    assert response["Content-Type"] == SIREN_MEDIA_TYPE
    assert response.json()["class"] == ["command"]
    assert response.json()["properties"]["openapi"] == "3.1.0"


def test_siren_projects_missing_resources_as_errors(client: Client) -> None:
    response = client.get("/siren/not-found")

    assert response.status_code == 404
    assert response["Content-Type"] == SIREN_MEDIA_TYPE
    assert response.json()["class"] == ["error"]
    assert response.json()["properties"] == {"detail": "Request failed."}
    assert response.json()["links"][0]["href"] == "http://testserver/siren/not-found"


@pytest.mark.django_db
def test_siren_projects_validation_errors(client: Client) -> None:
    response = client.post("/siren/scaffoldings", data={}, content_type="application/json")

    assert response.status_code == 422
    assert response["Content-Type"] == SIREN_MEDIA_TYPE
    assert response.json()["class"] == ["error"]
    assert response.json()["properties"] == {"detail": "Request failed."}
