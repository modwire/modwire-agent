class ReadApiMixin:
    def get_record(self, record_id: str):
        return self.client.get(f"/api/records/{record_id}")

    def get_section(self, section_id: str):
        return self.client.get(f"/api/sections/{section_id}")

    def list_sections(self):
        return self.client.get("/api/sections")

    def list_tags(self):
        return self.client.get("/api/tags")

    def search_text(self, query: str):
        return self.client.get(f"/api/records/search/text?q={query}")

    def search_semantic(self, query: str):
        return self.client.get(f"/api/records/search/semantic?q={query}")

    def rename_record(self, record_id: str, title: str, headers: dict[str, str]):
        return self.client.patch(f"/api/records/{record_id}", data={"title": title}, content_type="application/json", headers=headers)

    def archive_record(self, record_id: str, headers: dict[str, str]):
        return self.client.delete(f"/api/records/{record_id}", headers=headers)
