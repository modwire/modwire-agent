#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import yaml
from jinja2 import Environment, StrictUndefined

SOURCES = (
    (
        "Django API Project",
        "Production-ready Django Ninja API project.",
        "Python",
        "shared/packages/projects/django-api",
    ),
    (
        "React TypeScript Project",
        "Tested React, TypeScript, Vite, and Material UI application.",
        "TypeScript",
        "shared/packages/projects/react-typescript",
    ),
    (
        "Django API Application",
        "CRUD-ready Django API application module.",
        "Python",
        "shared/packages/modules/django-api-app",
    ),
    (
        "Python Layered Application",
        "Layered Python application module.",
        "Python",
        "shared/packages/modules/python-layered",
    ),
    (
        "Hexagonal Application",
        "Ports-and-adapters application module for TypeScript and Python.",
        "TypeScript",
        "shared/packages/modules/hexagonal",
    ),
)


class Api:
    def __init__(self, root: str, key: str):
        self.root = root
        self.key = key
        self.entry = self.request(root)

    def request(self, url: str, body: dict | None = None, method: str | None = None):
        data = json.dumps(body).encode() if body is not None else None
        request = Request(
            url,
            data=data,
            method=method or ("POST" if body is not None else "GET"),
            headers={
                "apikey": self.key,
                "Accept": "application/vnd.siren+json",
                "Content-Type": "application/json",
            },
        )
        try:
            with urlopen(request) as response:
                return json.load(response) if response.status != 204 else None
        except HTTPError as error:
            raise RuntimeError(f"{error.code} {url}: {error.read().decode()}") from error

    @staticmethod
    def link(document: dict, relation: str) -> str:
        return next(link["href"] for link in document["links"] if relation in link["rel"])

    @staticmethod
    def action(document: dict, name: str) -> str:
        return next(action["href"] for action in document["actions"] if action["name"] == name)

    def collection(self, relation: str) -> dict:
        return self.request(self.link(self.entry, relation))


def variable_type(question: dict) -> str:
    declared = question.get("type", "str")
    if declared != "yaml":
        return declared
    default = question.get("default")
    return "list" if isinstance(default, list) else "dict" if isinstance(default, dict) else "str"


def words(value) -> list[str]:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(value))
    return [word.lower() for word in re.findall(r"[A-Za-z0-9]+", text)]


def sample_default(name: str, question: dict, context: dict):
    if "default" in question:
        default = question["default"]
        if isinstance(default, str) and "{{" in default:
            environment = Environment(undefined=StrictUndefined)
            environment.filters.update(
                snake=lambda value: "_".join(words(value)),
                pascal=lambda value: "".join(word.capitalize() for word in words(value)),
            )
            return environment.from_string(default).render(context)
        return default
    samples = {
        "app_name": "sample_app",
        "model_name": "SampleItem",
        "module_name": "sample_module",
    }
    return samples.get(name, f"sample_{name}")


def import_source(api: Api, root: Path, source, language_ids: dict[str, str]) -> dict:
    name, description, language, relative = source
    directory = root / relative
    manifest = yaml.safe_load((directory / "copier.yml").read_text())

    scaffoldings = api.collection("scaffoldings")
    for entity in scaffoldings.get("entities", []):
        if entity.get("properties", {}).get("name") != name:
            continue
        resource = api.request(api.link(entity, "self"))
        api.request(api.action(resource, "delete_scaffolding"), method="DELETE")
        break
    scaffoldings = api.collection("scaffoldings")
    created = api.request(
        api.action(scaffoldings, "create_scaffolding"),
        {"language_id": language_ids[language], "name": name, "description": description},
    )["properties"]

    variables = api.collection("variables")
    create_variable = api.action(variables, "create_variable")
    variable_count = 0
    resolved_defaults = {}
    for variable_name, question in manifest.items():
        if variable_name.startswith("_") or not isinstance(question, dict):
            continue
        default = sample_default(variable_name, question, resolved_defaults)
        resolved_defaults[variable_name] = default
        api.request(
            create_variable,
            {
                "scaffolding_id": created["id"],
                "name": variable_name,
                "type": variable_type(question),
                "description": question.get("help", variable_name.replace("_", " ").title()),
                "default_value": default,
                "required": "default" not in question,
            },
        )
        variable_count += 1

    templates = api.collection("templates")
    create_template = api.action(templates, "create_template")
    template_count = 0
    for template in sorted((directory / manifest.get("_subdirectory", "templates")).rglob("*")):
        if not template.is_file():
            continue
        relative_path = template.relative_to(directory / manifest.get("_subdirectory", "templates")).as_posix()
        suffix = manifest.get("_templates_suffix", ".jinja")
        if relative_path.endswith(suffix):
            relative_path = relative_path[: -len(suffix)]
        content = template.read_text()
        relative_path = relative_path.replace("{{ model_snake_name }}", "{{ model_name | snake }}")
        content = content.replace("{{ model_snake_name }}", "{{ model_name | snake }}")
        content = content.replace("{{ model_pascal_name }}", "{{ model_name | pascal }}")
        if not content.strip():
            content = "# Generated package marker.\n" if relative_path.endswith(".py") else "// Generated file.\n"
        api.request(
            create_template,
            {
                "scaffolding_id": created["id"],
                "relative_path": relative_path,
                "file_content": content,
            },
        )
        template_count += 1

    return {"id": created["id"], "name": name, "variables": variable_count, "templates": template_count}


def main():
    parser = argparse.ArgumentParser(description="Import repository Copier scaffolds through the hypermedia API.")
    parser.add_argument("--api", required=True, help="Authenticated API entry-point URL.")
    parser.add_argument("--key", required=True, help="API key.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root.")
    parser.add_argument("--python-language-id", required=True)
    parser.add_argument("--typescript-language-id", required=True)
    args = parser.parse_args()

    api = Api(args.api, args.key)
    languages = {"Python": args.python_language_id, "TypeScript": args.typescript_language_id}
    imported = [import_source(api, args.root, source, languages) for source in SOURCES]
    print(json.dumps(imported, indent=2))


if __name__ == "__main__":
    main()
