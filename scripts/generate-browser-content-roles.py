from __future__ import annotations

import os
import sys
from pathlib import Path

import django

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "browser/src/models/recordContent.generated.ts"
sys.path.insert(0, str(ROOT))


def render() -> str:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    django.setup()

    from records.models.content import Content

    members = "\n".join(f'  {role.name}: "{role.value}",' for role in Content.Role)
    return f'''// Generated from records.models.content.Content.Role. Do not edit by hand.
export const CONTENT_ROLE = {{
{members}
}} as const;

type ContentRole = typeof CONTENT_ROLE[keyof typeof CONTENT_ROLE];
type ContentMetadata = Record<string, unknown>;

type TextContent = {{
  role: Exclude<ContentRole, typeof CONTENT_ROLE.LIST>;
  content: string;
  language: string;
  metadata: ContentMetadata;
}};

type ListContent = {{
  role: typeof CONTENT_ROLE.LIST;
  content: string[];
  language: string;
  metadata: ContentMetadata;
}};

export type RecordContent = TextContent | ListContent;
'''


if __name__ == "__main__":
    TARGET.write_text(render())
