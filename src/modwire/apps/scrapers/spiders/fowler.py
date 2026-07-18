from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any
from urllib.parse import urlparse, urlunparse

from scrapy import Spider
from scrapy.http import TextResponse

from modwire.apps.records.models.content import Content
from modwire.apps.scrapers.items import ScrapedContent, ScrapedRecord

ARCHITECTURE_URL = "https://martinfowler.com/architecture/"
AGILE_URL = "https://martinfowler.com/agile.html"
SKIPPED_PATH_PREFIXES = ("/about", "/books", "/faq", "/feed", "/fragments", "/photos", "/tags", "/videos")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def unique(values: Iterable[str]) -> list[str]:
    result = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


class FowlerSpider(Spider):
    name = "fowler"
    allowed_domains = ["martinfowler.com"]
    start_urls = [ARCHITECTURE_URL]
    base_tag_names = ["Martin Fowler"]

    def __init__(self, limit: int, include_images: bool = True, **kwargs: Any):
        super().__init__(**kwargs)
        self.limit = limit
        self.include_images = include_images
        self._scheduled = 0

    def parse(self, response: TextResponse):
        for href in self.article_links(response):
            if self.limit and self._scheduled >= self.limit:
                break
            self._scheduled += 1
            yield response.follow(href, callback=self.parse_article)

    def parse_article(self, response: TextResponse):
        title = self.title(response)
        content = self.content_blocks(response)
        yield ScrapedRecord(
            title=title,
            description=self.description(response, content),
            sources=[response.url],
            content=content,
            tag_names=unique([*self.base_tag_names, *self.article_tags(response)]),
        )

    def article_links(self, response: TextResponse) -> list[str]:
        links = []
        for href in response.css("main a::attr(href)").getall():
            url = self.canonical_url(response.urljoin(href))
            if self.is_article_url(url) and url not in links:
                links.append(url)
        return links

    def is_article_url(self, url: str) -> bool:
        parsed = urlparse(url)
        path = parsed.path.rstrip("/") or "/"
        if parsed.netloc and parsed.netloc != "martinfowler.com":
            return False
        if path in {"/", "/architecture", "/agile.html"}:
            return False
        if any(path.startswith(prefix) for prefix in SKIPPED_PATH_PREFIXES):
            return False
        return path.endswith(".html") or "." not in path.rsplit("/", maxsplit=1)[-1]

    def title(self, response: TextResponse) -> str:
        title = clean_text(" ".join(response.css("main h1:first-of-type ::text").getall()))
        meta_title = response.css("meta[property='og:title']::attr(content)").get("")
        return (title or clean_text(meta_title) or "Untitled").removeprefix("bliki: ").strip()

    def description(self, response: TextResponse, content: list[ScrapedContent]) -> str:
        meta_description = response.css("meta[property='og:description']::attr(content)").get("")
        if meta_description:
            return clean_text(meta_description)
        for block in content:
            if block.role in {Content.Role.PARAGRAPH, Content.Role.LIST}:
                return block.content.splitlines()[0]
        return self.title(response)

    def article_tags(self, response: TextResponse) -> list[str]:
        return [
            clean_text(text).title()
            for text in response.css("main .frontMatter .tags a::text").getall()
            if clean_text(text)
        ]

    def content_blocks(self, response: TextResponse) -> list[ScrapedContent]:
        blocks = [ScrapedContent(Content.Role.HEADING, self.title(response), "text", {"source_url": response.url})]
        roots = response.xpath(
            "//main//*[contains(concat(' ', normalize-space(@class), ' '), ' paperBody ') "
            "or contains(concat(' ', normalize-space(@class), ' '), ' appendix ')]"
        ) or response.xpath("//main")

        for root in roots:
            for element in root.xpath(
                ".//*[self::h2 or self::h3 or self::h4 or self::p or self::ul "
                "or self::ol or self::pre or self::img]"
            ):
                blocks.extend(self.content_from_element(response, element))
        return blocks

    def content_from_element(self, response: TextResponse, element) -> list[ScrapedContent]:
        tag = element.root.tag.lower()
        text = clean_text(" ".join(element.xpath(".//text()").getall()))
        if tag in {"h2", "h3", "h4"} and text:
            return [ScrapedContent(Content.Role.SUBHEADING, text, "text", {"source_url": response.url})]
        if tag == "p" and text:
            return [ScrapedContent(Content.Role.PARAGRAPH, text, "text", {"source_url": response.url})]
        if tag in {"ul", "ol"}:
            items = [clean_text(" ".join(item.xpath(".//text()").getall())) for item in element.xpath("./li")]
            content = [item for item in items if item]
            return [ScrapedContent(Content.Role.LIST, content, "text", {"source_url": response.url})] if content else []
        if tag == "pre":
            source = "\n".join(element.xpath(".//text()").getall()).strip()
            return (
                [ScrapedContent(Content.Role.SNIPPET, source, "text", {"source_url": response.url})]
                if source
                else []
            )
        if tag == "img" and self.include_images:
            src = element.attrib.get("src")
            if src:
                url = response.urljoin(src)
                return [
                    ScrapedContent(
                        Content.Role.IMAGE,
                        url,
                        "url",
                        {"source_url": url, "alt": clean_text(element.attrib.get("alt", ""))},
                    )
                ]
        return []

    def canonical_url(self, url: str) -> str:
        parsed = urlparse(url)
        return urlunparse(parsed._replace(fragment="", query=""))


class FowlerArchitectureSpider(FowlerSpider):
    name = "fowler-architecture"
    start_urls = [ARCHITECTURE_URL]
    base_tag_names = ["Martin Fowler", "Architecture"]


class FowlerAgileSpider(FowlerSpider):
    name = "fowler-agile"
    start_urls = [AGILE_URL]
    base_tag_names = ["Martin Fowler", "Agile"]
