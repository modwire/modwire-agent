from django.test import TestCase
from dirty_equals import IsPartialDict, IsStr


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
        self.assertEqual(
            response.json(),
            IsPartialDict(id=None, dry_run=True, plan=IsPartialDict(scaffolding="create")),
        )

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
        self.assertEqual(response.json(), IsPartialDict(id=IsStr(min_length=1), name="starter"))

        bundle = self.client.get(f"/api/scaffoldings/{response.json()['id']}/bundle")
        self.assertEqual(bundle.status_code, 200)
        self.assertEqual(bundle.json(), IsPartialDict(name="starter", variables=[], templates=[]))
