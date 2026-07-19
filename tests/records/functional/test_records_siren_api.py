from dirty_equals import IsUUID

from .api import RecordsApiTestCase


class RecordsSirenApiScenarios(RecordsApiTestCase):
    def test_browses_a_published_record_by_tag(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "Siren contract", "rule")
        tag = self.create_tag("Hypermedia")
        self.set_record_tags(record["id"], [tag["id"]])
        self.replace_content(record["id"], self.valid_rule_markdown())
        self.assertEqual(self.publish_record(record["id"]).status_code, 200)

        collection = self.client.get("/siren/records?tag=hypermedia")
        entity = self.client.get(f"/siren/records/{record['id']}")

        self.assertEqual(collection.status_code, 200)
        self.assertEqual(collection["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(collection.json()["class"], ["collection", "record"])
        self.assertEqual(
            collection.json()["entities"][0]["properties"],
            {"id": IsUUID, "title": "Siren contract", "reason": "tag: hypermedia"},
        )
        self.assertEqual(collection.json()["actions"][0]["name"], "list_siren_records")

        self.assertEqual(entity.status_code, 200)
        self.assertEqual(entity["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(entity.json()["class"], ["record"])
        self.assertEqual(entity.json()["properties"]["title"], "Siren contract")
        self.assertEqual(entity.json()["properties"]["tags"], ["hypermedia"])
        self.assertEqual(entity.json()["actions"][0]["name"], "get_siren_record")
