from dirty_equals import IsList, IsPartialDict
from django.test import TestCase


class LanguagesApiScenarios(TestCase):
    def test_lists_the_supported_language_catalog(self) -> None:
        response = self.client.get("/api/languages")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            IsList(
                IsPartialDict(id="mermaid", executable="mmdc"),
                IsPartialDict(id="php", executable="php"),
                IsPartialDict(id="python", executable="python"),
                IsPartialDict(id="typescript", executable="tsc"),
            ),
        )

    def test_reads_one_language_and_rejects_an_unknown_identifier(self) -> None:
        language = self.client.get("/api/languages/PYTHON")
        unknown = self.client.get("/api/languages/rust")

        self.assertEqual(language.status_code, 200)
        self.assertEqual(
            language.json(),
            IsPartialDict(id="python", name="Python", source_extensions=[".py"], aliases=["py"]),
        )
        self.assertEqual(unknown.status_code, 404)

    def test_exposes_each_catalog_entry_with_its_version_provider_and_tools(self) -> None:
        response = self.client.get("/api/languages/typescript")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            IsPartialDict(
                id="typescript",
                version_provider=IsPartialDict(kind="npm", result_path=["version"]),
                package_managers=IsList(IsPartialDict(id="npm", supports_workspaces=True)),
                tools=IsList(
                    IsPartialDict(id="typescript"),
                    IsPartialDict(id="eslint"),
                    IsPartialDict(id="prettier"),
                    IsPartialDict(id="vitest"),
                    IsPartialDict(id="vitest-v8"),
                    IsPartialDict(id="tsx"),
                    IsPartialDict(id="typedoc"),
                ),
            ),
        )
