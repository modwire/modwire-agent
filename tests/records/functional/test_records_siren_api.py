from dirty_equals import IsUUID

from .api import RecordsApiTestCase


class RecordsSirenApiScenarios(RecordsApiTestCase):
    def test_searches_records_through_siren(self) -> None:
        section = self.create_section("Search", ["rule"])
        record = self.create_record(section["id"], "HTTP contract", "rule")
        self.replace_content(record["id"], self.valid_rule_markdown())
        self.publish_record(record["id"])

        text = self.client.get("/siren/records/search/text?q=HTTP")
        semantic = self.client.get("/siren/records/search/semantic?q=HTTP%20contract")

        self.assertEqual(text.status_code, 200)
        self.assertEqual(text.json()["entities"][0]["properties"]["reason"], "text")
        self.assertEqual(semantic.status_code, 200)
        self.assertEqual(semantic.json()["entities"][0]["properties"]["reason"], "semantic")

    def test_manages_record_history_proposals_and_lifecycle_through_siren(self) -> None:
        section = self.create_section("Siren management", ["rule"])
        record = self.create_record(section["id"], "Original", "rule")
        headers = self.agent_headers()

        renamed = self.client.patch(f"/siren/records/{record['id']}", data={"title": "Renamed"}, content_type="application/json", headers=headers)
        self.assertEqual(renamed.status_code, 200)
        self.assertEqual(renamed.json()["properties"]["title"], "Renamed")

        replaced = self.client.put(f"/siren/records/{record['id']}/content", data={"markdown": self.valid_rule_markdown()}, content_type="application/json", headers=headers)
        self.assertEqual(replaced.status_code, 200)
        revisions = self.client.get(f"/siren/records/{record['id']}/content-revisions")
        self.assertEqual(revisions.status_code, 200)
        self.assertEqual(revisions.json()["entities"][0]["properties"]["markdown"], self.valid_rule_markdown())

        proposal = self.client.post(f"/siren/records/{record['id']}/content-proposals", data={"markdown": self.valid_rule_markdown()}, content_type="application/json", headers=headers)
        self.assertEqual(proposal.status_code, 200)
        proposals = self.client.get(f"/siren/records/{record['id']}/content-proposals")
        self.assertEqual(proposals.status_code, 200)
        proposal_id = proposals.json()["entities"][0]["properties"]["id"]
        resolved = self.client.patch(f"/siren/records/{record['id']}/content-proposals/{proposal_id}", data={"status": "accepted"}, content_type="application/json", headers=self.user_headers())
        self.assertEqual(resolved.status_code, 200)
        self.assertEqual(resolved.json()["properties"]["status"], "accepted")

        archived = self.client.delete(f"/siren/records/{record['id']}", headers=headers)
        self.assertEqual(archived.status_code, 204)

    def test_agent_can_create_and_enrich_records_through_siren_actions(self) -> None:
        headers = self.agent_headers()
        section_response = self.client.post(
            "/siren/sections",
            data={"title": "Agent work", "allowed_kinds": ["rule"]},
            content_type="application/json",
            headers=headers,
        )
        self.assertEqual(section_response.status_code, 200)
        section = section_response.json()["properties"]
        self.assertEqual(section["title"], "Agent work")

        record_response = self.client.post(
            f"/siren/sections/{section['id']}/records",
            data={"title": "Agent-created rule", "kind": "rule"},
            content_type="application/json",
            headers=headers,
        )
        self.assertEqual(record_response.status_code, 200)
        record = record_response.json()["properties"]
        self.assertEqual(record["title"], "Agent-created rule")

        tag_response = self.client.post(
            "/siren/tags",
            data={"name": "agent"},
            content_type="application/json",
            headers=headers,
        )
        self.assertEqual(tag_response.status_code, 200)
        tag_id = tag_response.json()["entities"][0]["properties"]["id"]

        tagged = self.client.put(
            f"/siren/records/{record['id']}/tags",
            data={"tag_ids": [tag_id]},
            content_type="application/json",
            headers=headers,
        )
        self.assertEqual(tagged.status_code, 200)
        self.assertEqual(tagged.json()["properties"]["tags"], ["agent"])

        content = self.client.put(
            f"/siren/records/{record['id']}/content",
            data={"markdown": self.valid_rule_markdown()},
            content_type="application/json",
            headers=headers,
        )
        self.assertEqual(content.status_code, 200)
        self.assertEqual(content.json()["properties"]["id"], record["id"])

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
