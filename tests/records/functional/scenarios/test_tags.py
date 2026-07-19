from ..api import RecordsApiTestCase


class TagScenarios(RecordsApiTestCase):
    def test_creates_a_normalized_tag(self) -> None:
        tag = self.create_tag(" Testing ")

        self.assertEqual(tag["name"], "testing")
