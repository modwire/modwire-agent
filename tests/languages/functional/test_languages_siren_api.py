from django.test import TestCase


class LanguagesSirenApiScenarios(TestCase):
    def test_exposes_a_siren_entry_point_and_languages_collection(self) -> None:
        root = self.client.get("/siren/")
        schema = self.client.get("/siren/openapi.json")
        collection = self.client.get("/siren/languages")

        self.assertEqual(root.status_code, 200)
        self.assertEqual(root["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(root.json()["class"], ["api", "entry-point"])
        self.assertEqual(root.json()["links"][0]["href"], "http://testserver/siren/")
        self.assertEqual(root.json()["links"][1]["href"], "http://testserver/siren/languages")

        self.assertEqual(schema.status_code, 200)
        self.assertEqual(schema["Content-Type"], "application/vnd.oai.openapi+json;version=3.1")
        resource = schema.json()["paths"]["/siren/languages/{language_id}"]["x-siren-resource"]
        self.assertEqual(resource["name"], "language")

        self.assertEqual(collection.status_code, 200)
        self.assertEqual(collection["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(collection.json()["class"], ["collection", "language"])
        self.assertEqual(collection.json()["entities"][0]["properties"]["id"], "mermaid")
        self.assertEqual(collection.json()["actions"][0]["name"], "list_siren_languages")

    def test_exposes_a_siren_language_entity(self) -> None:
        response = self.client.get("/siren/languages/python")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["language"])
        self.assertEqual(response.json()["properties"]["id"], "python")
        self.assertEqual(response.json()["links"][0]["href"], "http://testserver/siren/languages/python")
        self.assertEqual(response.json()["actions"][0]["name"], "get_siren_language")
