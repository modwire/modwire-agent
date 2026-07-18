import pytest

from .support import EndpointAssertions

pytestmark = pytest.mark.django_db


class TestLanguageCollection(EndpointAssertions):
    def test_languages_are_siren_collection_entities(self, client, auth):
        document = self.siren(self.api(client, auth).get("/api/languages")).assert_classes(
            "collection",
            "language",
        )

        document.assert_actions(["list_languages"])
        languages = document.embedded_properties("language")
        assert languages
        assert any(language["id"] == "python" for language in languages)
