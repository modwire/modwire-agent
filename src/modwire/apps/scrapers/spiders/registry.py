from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scrapy import Spider

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CACHE_ROOT = PROJECT_ROOT / ".scrapy"


@dataclass(frozen=True)
class ScrapeSource:
    name: str
    spider: type[Spider]
    settings_overrides: dict[str, Any]
    section_title: str
    section_description: str
    section_tag_names: list[str]


def source_settings(*, name: str, user_agent: str) -> dict[str, Any]:
    return {
        "BOT_NAME": f"modwire_{name}",
        "USER_AGENT": user_agent,
        "HTTPCACHE_DIR": str(CACHE_ROOT / name / "httpcache"),
    }


def list_sources() -> dict[str, ScrapeSource]:
    from modwire.apps.scrapers.spiders.fowler import FowlerAgileSpider, FowlerArchitectureSpider
    from modwire.apps.scrapers.spiders.sourcemaking import (
        SourceMakingCodeSmellsSpider,
        SourceMakingDesignPatternsSpider,
        SourceMakingRefactoringsSpider,
    )

    sources = [
        ScrapeSource(
            name="fowler-agile",
            spider=FowlerAgileSpider,
            settings_overrides=source_settings(
                name="fowler",
                user_agent="ModwireRecordsFowlerBot/0.1 (+https://martinfowler.com/)",
            ),
            section_title="Agile Software Development",
            section_description="Agile software development articles scraped from martinfowler.com.",
            section_tag_names=["Agile", "Martin Fowler"],
        ),
        ScrapeSource(
            name="fowler-architecture",
            spider=FowlerArchitectureSpider,
            settings_overrides=source_settings(
                name="fowler",
                user_agent="ModwireRecordsFowlerBot/0.1 (+https://martinfowler.com/)",
            ),
            section_title="Software Architecture",
            section_description="Software architecture articles scraped from martinfowler.com.",
            section_tag_names=["Architecture", "Martin Fowler"],
        ),
        ScrapeSource(
            name="sourcemaking-design-patterns",
            spider=SourceMakingDesignPatternsSpider,
            settings_overrides=source_settings(
                name="sourcemaking",
                user_agent="ModwireRecordsSourceMakingBot/0.1 (+https://sourcemaking.com/)",
            ),
            section_title="Design Patterns",
            section_description="Design pattern catalog scraped from SourceMaking.",
            section_tag_names=["Design Patterns", "SourceMaking"],
        ),
        ScrapeSource(
            name="sourcemaking-code-smells",
            spider=SourceMakingCodeSmellsSpider,
            settings_overrides=source_settings(
                name="sourcemaking",
                user_agent="ModwireRecordsSourceMakingBot/0.1 (+https://sourcemaking.com/)",
            ),
            section_title="Code Smells",
            section_description="Code smell catalog scraped from SourceMaking.",
            section_tag_names=["Code Smells", "SourceMaking", "Refactoring"],
        ),
        ScrapeSource(
            name="sourcemaking-refactorings",
            spider=SourceMakingRefactoringsSpider,
            settings_overrides=source_settings(
                name="sourcemaking",
                user_agent="ModwireRecordsSourceMakingBot/0.1 (+https://sourcemaking.com/)",
            ),
            section_title="Refactoring Techniques",
            section_description="Refactoring technique catalog scraped from SourceMaking.",
            section_tag_names=["Refactoring Techniques", "SourceMaking", "Refactoring"],
        ),
    ]
    return {source.name: source for source in sources}


def get_source(name: str) -> ScrapeSource:
    sources = list_sources()
    try:
        return sources[name]
    except KeyError as error:
        known = ", ".join(sorted(sources))
        raise ValueError(f"Unknown scrape source '{name}'. Known sources: {known}") from error
