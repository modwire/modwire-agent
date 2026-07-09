from __future__ import annotations

import logging

from django.core.management.base import BaseCommand, CommandError
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from records.importing import import_scraped_records
from scrapers.spiders.registry import get_source, list_sources


class Command(BaseCommand):
    help = "Scrape records from a configured source and import them into records."

    def add_arguments(self, parser):
        parser.add_argument("source", nargs="?", help="Scrape source name.")
        parser.add_argument("--list-sources", action="store_true", help="List sources and exit.")
        parser.add_argument("--limit", type=int, default=0, help="Maximum source records to crawl; 0 means all.")
        parser.add_argument("--dry-run", action="store_true", help="Scrape without writing records.")
        parser.add_argument("--no-update", action="store_true", help="Skip existing records.")
        parser.add_argument("--no-images", action="store_true", help="Do not fetch image assets.")
        parser.add_argument("--section-title", default="", help="Override section title.")
        parser.add_argument("--section-description", default="", help="Override section description.")

    def handle(self, *args, **options):
        sources = list_sources()
        if options["list_sources"]:
            for name in sorted(sources):
                self.stdout.write(name)
            return

        source_name = options["source"]
        if not source_name:
            raise CommandError("Provide a scrape source or use --list-sources.")

        try:
            source = get_source(source_name)
        except ValueError as error:
            raise CommandError(str(error)) from error

        scraped_records = self.run_spider(
            source.spider,
            settings_module=source.settings_module,
            limit=options["limit"],
            include_images=not options["no_images"],
            verbosity=options["verbosity"],
        )

        if options["dry_run"]:
            self.stdout.write(f"Scraped {len(scraped_records)} records from {source.name}.")
            for record in scraped_records[:10]:
                self.stdout.write(f"- {record.title} ({len(record.content)} content blocks)")
            return

        result = import_scraped_records(
            section_title=options["section_title"] or source.section_title,
            section_description=options["section_description"] or source.section_description,
            section_tag_names=source.section_tag_names,
            records=scraped_records,
            update_existing=not options["no_update"],
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(scraped_records)} records from {source.name}: "
                f"{result.created} created, {result.updated} updated, {result.skipped} skipped."
            )
        )

    def run_spider(
        self,
        spider,
        *,
        settings_module: str,
        limit: int,
        include_images: bool,
        verbosity: int,
    ) -> list:
        items: list = []
        settings = Settings()
        settings.setmodule(settings_module)
        settings.set("LOG_ENABLED", verbosity > 1, priority="cmdline")
        logging.getLogger("scrapy").setLevel(logging.INFO if verbosity > 1 else logging.WARNING)
        process = CrawlerProcess(settings=settings)
        crawler = process.create_crawler(spider)
        crawler.signals.connect(
            lambda item, response, spider: items.append(item),
            signal=signals.item_scraped,
            weak=False,
        )
        process.crawl(crawler, limit=limit, include_images=include_images)
        process.start()
        return items
