from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from modwire.apps.records.models.content import Content


@dataclass(frozen=True)
class ScrapedContent:
    role: Content.Role
    content: str | list[str]
    language: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_record_content(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "language": self.language or "text",
            "metadata": self.metadata or {"source": "scraper"},
        }


@dataclass(frozen=True)
class ScrapedRecord:
    title: str
    description: str
    sources: list[str]
    content: list[ScrapedContent]
    tag_names: list[str]
