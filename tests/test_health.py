import pytest


@pytest.mark.django_db
def test_health_reports_the_database_dependency(client):
    response = client.get("/health/?format=json")

    assert response.status_code == 200
    assert response.json() == {"Database(alias='default')": "OK"}
