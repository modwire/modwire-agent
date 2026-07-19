from dirty_equals import IsInt, IsPartialDict, IsStr
from django.test import TestCase


class ApiKeyScenarios(TestCase):
    def test_creates_a_key_once_and_returns_only_the_public_contract(self) -> None:
        response = self.client.post(
            "/api/api_keys",
            data={"name": " automation "},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            IsPartialDict(
                id=IsInt(gt=0),
                name="automation",
                created_at=IsStr(),
                updated_at=IsStr(),
                key=IsStr(min_length=20),
            ),
        )

    def test_rejects_a_blank_name_and_undeclared_fields(self) -> None:
        blank = self.client.post(
            "/api/api_keys",
            data={"name": " "},
            content_type="application/json",
        )
        extra = self.client.post(
            "/api/api_keys",
            data={"name": "automation", "is_active": False},
            content_type="application/json",
        )

        self.assertEqual(blank.status_code, 422)
        self.assertEqual(extra.status_code, 422)
