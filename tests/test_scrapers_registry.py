from __future__ import annotations

from scrapers.spiders.registry import get_source, list_sources


def test_scraper_sources_are_registered_with_local_spiders():
    sources = list_sources()

    assert sorted(sources) == [
        "fowler-agile",
        "fowler-architecture",
        "sourcemaking-code-smells",
        "sourcemaking-design-patterns",
        "sourcemaking-refactorings",
    ]
    assert all(source.spider.__module__.startswith("scrapers.spiders.") for source in sources.values())


def test_scraper_source_uses_shared_settings_overrides():
    source = get_source("fowler-architecture")

    assert source.settings_overrides["BOT_NAME"] == "modwire_fowler"
    assert source.settings_overrides["USER_AGENT"].startswith("ModwireRecordsFowlerBot/")
    assert source.settings_overrides["HTTPCACHE_DIR"].endswith(".scrapy/fowler/httpcache")
