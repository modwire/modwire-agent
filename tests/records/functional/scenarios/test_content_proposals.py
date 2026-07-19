from dirty_equals import IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class ContentProposalScenarios(RecordsApiTestCase):
    def test_accepting_an_agents_content_proposal_creates_an_authored_revision(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        proposed = self.create_content_proposal(record["id"], self.valid_rule_markdown(), self.agent_headers())

        listed = self.list_content_proposals(record["id"])

        accepted = self.resolve_content_proposal(proposed.json()["id"], "accepted", self.user_headers())
        revisions = self.list_content_revisions(record["id"])

        self.assertEqual(proposed.status_code, 201)
        self.assertEqual(proposed.json(), IsPartialDict(id=IsUUID, status="proposed"))
        self.assertEqual(listed.json()[0]["proposed_by_type"], "agent")
        self.assertEqual(accepted.status_code, 200)
        self.assertEqual(accepted.json(), IsPartialDict(id=IsUUID, status="accepted"))
        self.assertEqual(revisions.json()[0]["actor_type"], "agent")

    def test_rejecting_an_agents_content_proposal_does_not_create_a_revision(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        proposed = self.create_content_proposal(record["id"], self.valid_rule_markdown(), self.agent_headers())

        rejected = self.resolve_content_proposal(proposed.json()["id"], "rejected", self.user_headers())
        revisions = self.list_content_revisions(record["id"])

        self.assertEqual(rejected.status_code, 200)
        self.assertEqual(rejected.json(), IsPartialDict(id=IsUUID, status="rejected"))
        self.assertEqual(revisions.json(), [])
