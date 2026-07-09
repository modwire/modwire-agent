# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScraperSourcemakingItem:
    # define the fields for your item here like:
    # name: str | None = None
    pass


@dataclass(frozen=True)
class ScrapedContent:
    role: str
    content: str
    language: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_record_content(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "content": self.content,
            "language": self.language or "text",
            "metadata": self.metadata or {"source": "scraper_sourcemaking"},
        }


@dataclass(frozen=True)
class ScrapedRecord:
    title: str
    description: str
    sources: list[str]
    content: list[ScrapedContent]
    tag_names: list[str]
