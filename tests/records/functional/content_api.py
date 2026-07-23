class ContentApiMixin:
    def replace_content(self, record_id: str, markdown: str):
        return self.client.put(
            f"/api/records/{record_id}/content",
            data={"markdown": markdown},
            content_type="application/json",
            headers=self.agent_headers(),
        )

    def list_content_revisions(self, record_id: str):
        return self.client.get(f"/api/records/{record_id}/content-revisions")

    def valid_rule_markdown(self) -> str:
        return "## Rules\n\nUse HTTP.\n\n## Verification\n\nExercise the public API."
