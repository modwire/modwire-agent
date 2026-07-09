from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from scrapy import Spider

PROJECT_ROOT = Path(__file__).resolve().parents[2]
for project_dir in ("scraper_fowler", "scraper_sourcemaking"):
    path = str(PROJECT_ROOT / project_dir)
    if path not in sys.path:
        sys.path.insert(0, path)


@dataclass(frozen=True)
class ScrapeSource:
    name: str
    spider: type[Spider]
    settings_module: str
    section_title: str
    section_description: str
    section_tag_names: list[str]


def list_sources() -> dict[str, ScrapeSource]:
    from scraper_fowler.spiders.fowler import FowlerAgileSpider, FowlerArchitectureSpider
    from scraper_sourcemaking.spiders.sourcemaking import (
        SourceMakingCodeSmellsSpider,
        SourceMakingDesignPatternsSpider,
        SourceMakingRefactoringsSpider,
    )

    sources = [
        ScrapeSource(
            name="fowler-agile",
            spider=FowlerAgileSpider,
            settings_module="scraper_fowler.settings",
            section_title="Agile Software Development",
            section_description="Agile software development articles scraped from martinfowler.com.",
            section_tag_names=["Agile", "Martin Fowler"],
        ),
        ScrapeSource(
            name="fowler-architecture",
            spider=FowlerArchitectureSpider,
            settings_module="scraper_fowler.settings",
            section_title="Software Architecture",
            section_description="Software architecture articles scraped from martinfowler.com.",
            section_tag_names=["Architecture", "Martin Fowler"],
        ),
        ScrapeSource(
            name="sourcemaking-design-patterns",
            spider=SourceMakingDesignPatternsSpider,
            settings_module="scraper_sourcemaking.settings",
            section_title="Design Patterns",
            section_description="Design pattern catalog scraped from SourceMaking.",
            section_tag_names=["Design Patterns", "SourceMaking"],
        ),
        ScrapeSource(
            name="sourcemaking-code-smells",
            spider=SourceMakingCodeSmellsSpider,
            settings_module="scraper_sourcemaking.settings",
            section_title="Code Smells",
            section_description="Code smell catalog scraped from SourceMaking.",
            section_tag_names=["Code Smells", "SourceMaking", "Refactoring"],
        ),
        ScrapeSource(
            name="sourcemaking-refactorings",
            spider=SourceMakingRefactoringsSpider,
            settings_module="scraper_sourcemaking.settings",
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
