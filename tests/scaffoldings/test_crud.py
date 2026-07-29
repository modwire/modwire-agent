import pytest
from django.test import Client


@pytest.mark.django_db
def test_scaffolding_crud() -> None:
    client = Client()
    payload = {
        "language_id": "python",
        "name": "Package",
        "description": "Creates a Python package.",
        "spec": {
            "language": "python",
            "package": {"files": {"src/package/__init__.py": ""}},
        },
    }

    created = client.post("/api/scaffoldings", data=payload, content_type="application/json")

    assert created.status_code == 201
    scaffolding_id = created.json()["id"]

    listed = client.get("/api/scaffoldings")

    assert listed.status_code == 200
    assert listed.json()[0]["id"] == scaffolding_id

    fetched = client.get(f"/api/scaffoldings/{scaffolding_id}")

    assert fetched.status_code == 200
    assert fetched.json()["spec"] == payload["spec"]

    rendering = client.post(
        f"/api/scaffoldings/{scaffolding_id}/renderings",
        data={"parameters": {}},
        content_type="application/json",
    )

    assert rendering.status_code == 200
    assert rendering.json() == {"files": {"src/package/__init__.py": ""}}

    payload["name"] = "Renamed package"
    updated = client.put(f"/api/scaffoldings/{scaffolding_id}", data=payload, content_type="application/json")

    assert updated.status_code == 200
    assert updated.json()["name"] == "Renamed package"

    deleted = client.delete(f"/api/scaffoldings/{scaffolding_id}")

    assert deleted.status_code == 204
