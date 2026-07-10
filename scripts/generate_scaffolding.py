#!/usr/bin/env python3
import argparse
import json
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from shared.code import CodePackage, CopierArchive


def safe_destination(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"Unsafe generated path: {relative!r}")
    destination = root.joinpath(*path.parts)
    destination.resolve().relative_to(root.resolve())
    return destination


def main():
    parser = argparse.ArgumentParser(description="Fetch one generic API bundle, then render it locally with Copier.")
    parser.add_argument("--url", required=True, help="Scaffolding bundle action URL.")
    parser.add_argument("--key", required=True, help="API key.")
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--values", required=True, type=json.loads, help="JSON object of scaffolding values.")
    args = parser.parse_args()

    request = Request(
        args.url,
        method="GET",
        headers={
            "apikey": args.key,
            "Accept": "application/vnd.siren+json",
        },
    )
    try:
        with urlopen(request) as response:
            document = json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"Generation failed: {error.code} {error.read().decode()}") from error

    bundle = document["properties"]
    manifest = {"_min_copier_version": "9.0.0", "_templates_suffix": ".jinja", "_subdirectory": "templates"}
    for variable in bundle["variables"]:
        question = {
            "type": "yaml" if variable["type"] in {"list", "dict"} else variable["type"],
            "default": variable["default_value"],
            "help": variable["description"],
        }
        manifest[variable["name"]] = question
    templates = {f"{template['relative_path']}.jinja": template["file_content"] for template in bundle["templates"]}
    package = CopierArchive(manifest=manifest, templates=CodePackage(files=templates)).render(args.values)
    for relative in package.files:
        safe_destination(args.destination, relative)
    package.write_to_directory(args.destination)
    print(json.dumps({"destination": str(args.destination), "files": len(package.files)}, indent=2))


if __name__ == "__main__":
    main()
