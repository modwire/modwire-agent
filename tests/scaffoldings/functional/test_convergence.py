from django.test import TestCase

from modwire.scaffoldings.adapters.django.models.scaffolding import Scaffolding


class ScaffoldingConvergenceScenarios(TestCase):
    def test_dry_run_describes_creation_without_persisting(self) -> None:
        response = self.client.post(
            "/api/scaffoldings/converge",
            data={
                "language_id": "python",
                "name": "starter",
                "description": "A starter project.",
                "variables": [],
                "templates": [],
                "dry_run": True,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["plan"]["scaffolding"], "create")

    def test_persists_a_converged_scaffolding_and_exposes_its_bundle(self) -> None:
        response = self.client.post(
            "/api/scaffoldings/converge",
            data={
                "language_id": "python",
                "name": "starter",
                "description": "A starter project.",
                "variables": [],
                "templates": [],
                "dry_run": False,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        scaffolding = Scaffolding.objects.get(language_id="python", name="starter")
        bundle = self.client.get(f"/api/scaffoldings/{scaffolding.id}/bundle")
        self.assertEqual(bundle.status_code, 200)
        self.assertEqual(bundle.json()["name"], "starter")
