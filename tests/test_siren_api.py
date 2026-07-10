import pytest

from tokens.models.api_key import ApiKey


@pytest.fixture
def siren_client(client, db):
    _, secret = ApiKey.generate("siren-tests")
    client.defaults["HTTP_APIKEY"] = secret
    client.defaults["HTTP_ACCEPT"] = "application/vnd.siren+json"
    return client


def relation(document, rel):
    return next(link for link in document["links"] if rel in link["rel"])


def test_api_root_is_a_siren_entry_point(siren_client):
    response = siren_client.get("/api/")

    assert response.status_code == 200
    assert response["Content-Type"] == "application/vnd.siren+json"
    assert response.json()["class"] == ["api", "entry-point"]
    assert relation(response.json(), "records")["href"].endswith("/api/records")
    assert relation(response.json(), "browser")["href"].endswith("/browser/")


def test_collection_embeds_entities_and_advertises_actions(siren_client):
    response = siren_client.get("/api/tags")
    document = response.json()

    assert response["Content-Type"] == "application/vnd.siren+json"
    assert document["class"] == ["collection", "tag"]
    assert any(action["name"] == "create_tag" and action["method"] == "POST" for action in document["actions"])


def test_resource_has_absolute_related_links(siren_client):
    create = siren_client.post(
        "/api/tags", data={"name": "Architecture", "description": "Design"}, content_type="application/json"
    )
    document = create.json()

    assert document["class"] == ["tag"]
    assert relation(document, "self")["href"].startswith("http://testserver/")
    assert any(action["name"] == "partial_update_tag" for action in document["actions"])


def test_errors_use_problem_json(siren_client):
    response = siren_client.get("/api/tags/does-not-exist")

    assert response.status_code == 404
    assert response["Content-Type"] == "application/problem+json"
    assert response.json()["status"] == 404


def test_browser_route_explains_missing_build(client):
    response = client.get("/browser/")
    assert response.status_code in {200, 503}
