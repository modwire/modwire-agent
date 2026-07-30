import pytest
from django.test import Client


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    [
        "/api/records/missing",
        "/api/records/categories/missing",
        "/api/records/tags/missing",
    ],
)
def test_missing_records_return_not_found(path: str) -> None:
    response = Client().get(path)

    assert response.status_code == 404
    assert response.json() == {"detail": "Resource not found."}
