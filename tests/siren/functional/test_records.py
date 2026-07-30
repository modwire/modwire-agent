import pytest
from django.test import Client

SIREN_MEDIA_TYPE = "application/vnd.siren+json"


@pytest.mark.django_db
def test_siren_projects_an_empty_tag_collection() -> None:
    response = Client().get("/siren/records/tags")

    assert response.status_code == 200
    assert response["Content-Type"] == SIREN_MEDIA_TYPE
    assert response.json()["class"] == ["collection", "tag"]
    assert response.json().get("entities", []) == []


@pytest.mark.django_db
def test_siren_searches_records() -> None:
    response = Client().post(
        "/siren/records/search",
        data={"query": "missing", "limit": 5},
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response["Content-Type"] == SIREN_MEDIA_TYPE
    assert response.json()["class"] == ["collection", "record"]
    assert response.json().get("entities", []) == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    [
        "/siren/records/missing",
        "/siren/records/categories/missing",
        "/siren/records/tags/missing",
    ],
)
def test_siren_projects_missing_records_as_not_found(path: str) -> None:
    response = Client().get(path)

    assert response.status_code == 404
    assert response["Content-Type"] == SIREN_MEDIA_TYPE
    assert response.json()["class"] == ["error"]
    assert response.json()["properties"] == {"detail": "Resource not found."}
