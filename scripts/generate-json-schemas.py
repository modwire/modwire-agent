from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import django

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "schemas"
sys.path.insert(0, str(ROOT / "src"))


def render() -> dict[str, str]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modwire.core.settings")
    django.setup()

    from modwire.apps.records.api.content.schemas import ContentIn, ContentOut, ContentPatchIn
    from modwire.apps.records.api.schemas.content import ContentBlock, ContentMetadata

    models = {
        "content-block.schema.json": ContentBlock,
        "content-in.schema.json": ContentIn,
        "content-metadata.schema.json": ContentMetadata,
        "content-out.schema.json": ContentOut,
        "content-patch-in.schema.json": ContentPatchIn,
    }
    return {
        name: json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n"
        for name, model in models.items()
    }


if __name__ == "__main__":
    TARGET.mkdir(parents=True, exist_ok=True)
    for name, content in render().items():
        (TARGET / name).write_text(content)
