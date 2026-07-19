class ProposalsApiMixin:
    def create_content_proposal(self, record_id: str, markdown: str, headers: dict[str, str]):
        return self.client.post(f"/api/records/{record_id}/content-proposals", data={"markdown": markdown}, content_type="application/json", headers=headers)

    def resolve_content_proposal(self, proposal_id: str, status: str, headers: dict[str, str]):
        return self.client.patch(f"/api/content-proposals/{proposal_id}", data={"status": status}, content_type="application/json", headers=headers)

    def list_content_proposals(self, record_id: str):
        return self.client.get(f"/api/records/{record_id}/content-proposals")

    def user_headers(self) -> dict[str, str]:
        return {"X-Actor-Id": "test-user", "X-Actor-Type": "user"}
