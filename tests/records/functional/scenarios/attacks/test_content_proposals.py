from ...api import RecordsApiTestCase


class ContentProposalAttacks(RecordsApiTestCase):
    def test_rejects_a_users_direct_content_proposal(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")

        response = self.create_content_proposal(record["id"], self.valid_rule_markdown(), self.user_headers())

        self.assertEqual(response.status_code, 422)

    def test_rejects_an_agents_attempt_to_resolve_a_proposal(self) -> None:
        section = self.create_section("Architecture", ["rule"])
        record = self.create_record(section["id"], "API tests", "rule")
        proposal = self.create_content_proposal(record["id"], self.valid_rule_markdown(), self.agent_headers())

        response = self.resolve_content_proposal(proposal.json()["id"], "accepted", self.agent_headers())

        self.assertEqual(response.status_code, 422)
