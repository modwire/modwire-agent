from django.test import TestCase


class HealthScenarios(TestCase):
    def test_reports_database_readiness(self) -> None:
        response = self.client.get("/health/?format=json")

        self.assertEqual(response.json(), {"Database(alias='default')": "OK"})
