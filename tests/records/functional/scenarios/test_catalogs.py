from dirty_equals import IsList, IsPartialDict, IsUUID

from ..api import RecordsApiTestCase


class CatalogScenarios(RecordsApiTestCase):
    def test_lists_sections_and_tags_for_navigation(self) -> None:
        self.create_section("Architecture", ["rule"])
        self.create_tag("Testing")

        sections = self.list_sections()
        tags = self.list_tags()

        self.assertEqual(sections.status_code, 200)
        self.assertEqual(sections.json(), IsList(IsPartialDict(id=IsUUID, title="Architecture")))
        self.assertEqual(tags.status_code, 200)
        self.assertEqual(tags.json(), IsList(IsPartialDict(id=IsUUID, name="testing")))
