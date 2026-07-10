from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any
from urllib.parse import urlparse

from scrapy import Spider
from scrapy.http import TextResponse

from scrapers.items import ScrapedContent, ScrapedRecord

DESIGN_PATTERNS_URL = "https://sourcemaking.com/design_patterns"
CODE_SMELLS_URL = "https://sourcemaking.com/refactoring/smells"
REFACTORINGS_URL = "https://sourcemaking.com/refactoring/refactorings"
PATTERN_CATEGORY_SLUGS = {"creational_patterns", "structural_patterns", "behavioral_patterns"}
SMELL_CATEGORY_SLUGS = {
    "bloaters",
    "object-orientation-abusers",
    "change-preventers",
    "dispensables",
    "couplers",
    "other-smells",
}
REFACTORING_CATEGORY_SLUGS = {
    "composing-methods",
    "moving-features-between-objects",
    "organizing-data",
    "simplifying-conditional-expressions",
    "simplifying-method-calls",
    "dealing-with-generalisation",
}
STOP_HEADINGS = {
    "support our free website and own the ebook",
    "reading is boring",
    "code examples",
    "read next",
    "return",
}


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def unique(values: Iterable[str]) -> list[str]:
    result = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result


def is_stop_heading(value: str) -> bool:
    return clean_text(value).lower().strip(" !:") in STOP_HEADINGS


class SourceMakingSpider(Spider):
    name = "sourcemaking"
    allowed_domains = ["sourcemaking.com"]
    start_urls = [DESIGN_PATTERNS_URL]
    item_path_prefix = ("design_patterns",)
    excluded_item_slugs = PATTERN_CATEGORY_SLUGS
    base_tag_names = ["Design Pattern"]
    title_suffixes = (" Design Pattern",)

    def __init__(self, limit: int, include_images: bool = True, **kwargs: Any):
        super().__init__(**kwargs)
        self.limit = limit
        self.include_images = include_images
        self._scheduled = 0

    def parse(self, response: TextResponse):
        seen: set[str] = set()
        for href in response.css("a::attr(href)").getall():
            url = response.urljoin(href)
            if not self.is_item_url(url) or url in seen:
                continue
            if self.limit and self._scheduled >= self.limit:
                break
            seen.add(url)
            self._scheduled += 1
            yield response.follow(url, callback=self.parse_item)

    def parse_item(self, response: TextResponse):
        title = self.title(response)
        content = self.content_blocks(response)
        yield ScrapedRecord(
            title=title,
            description=self.description(content) or title,
            sources=[response.url],
            content=content,
            tag_names=unique([*self.base_tag_names, *self.category_tags(response)]),
        )

    def is_item_url(self, url: str) -> bool:
        parsed = urlparse(url)
        parts = [part for part in parsed.path.split("/") if part]
        if parsed.netloc and parsed.netloc != "sourcemaking.com":
            return False
        if len(parts) != len(self.item_path_prefix) + 1:
            return False
        if tuple(parts[: len(self.item_path_prefix)]) != self.item_path_prefix:
            return False
        return parts[-1] not in self.excluded_item_slugs

    def title(self, response: TextResponse) -> str:
        title = clean_text(" ".join(response.css("h1::text").getall()))
        for suffix in self.title_suffixes:
            title = title.removesuffix(suffix)
        return title or "Untitled"

    def category_tags(self, response: TextResponse) -> list[str]:
        tags = []
        for text in response.xpath("//h1/preceding::a/text()").getall():
            normalized = clean_text(text).lower()
            if normalized in {"refactoring", "design patterns", "code smells", "refactoring techniques"}:
                continue
            tags.append(clean_text(text).removesuffix(" patterns").title())
        return tags

    def content_blocks(self, response: TextResponse) -> list[ScrapedContent]:
        blocks = [ScrapedContent("heading", self.title(response), "text", {"source_url": response.url})]
        for element in response.xpath(
            "//h1/following::*[self::h2 or self::h3 or self::h4 or self::p "
            "or self::ul or self::ol or self::pre or self::img]"
        ):
            blocks.extend(self.content_from_element(response, element))
        return blocks

    def content_from_element(self, response: TextResponse, element) -> list[ScrapedContent]:
        tag = element.root.tag.lower()
        text = clean_text(" ".join(element.xpath(".//text()").getall()))
        if tag in {"h2", "h3", "h4"}:
            if is_stop_heading(text):
                return []
            return [ScrapedContent("subheading", text, "text", {"source_url": response.url})] if text else []
        if tag == "p" and text:
            return [ScrapedContent("paragraph", text, "text", {"source_url": response.url})]
        if tag in {"ul", "ol"}:
            items = [clean_text(" ".join(item.xpath(".//text()").getall())) for item in element.xpath("./li")]
            content = "\n".join(item for item in items if item)
            return [ScrapedContent("list", content, "text", {"source_url": response.url})] if content else []
        if tag == "pre":
            source = "\n".join(element.xpath(".//text()").getall()).strip()
            return [ScrapedContent("snippet", source, "text", {"source_url": response.url})] if source else []
        if tag == "img" and self.include_images:
            src = element.attrib.get("src")
            if src:
                url = response.urljoin(src)
                return [
                    ScrapedContent(
                        "image",
                        url,
                        "url",
                        {"source_url": url, "alt": clean_text(element.attrib.get("alt", ""))},
                    )
                ]
        return []

    def description(self, content: list[ScrapedContent]) -> str:
        for block in content:
            if block.role in {"paragraph", "list"}:
                return block.content.splitlines()[0]
        return ""


class SourceMakingDesignPatternsSpider(SourceMakingSpider):
    name = "sourcemaking-design-patterns"
    start_urls = [DESIGN_PATTERNS_URL]
    item_path_prefix = ("design_patterns",)
    excluded_item_slugs = PATTERN_CATEGORY_SLUGS
    base_tag_names = ["Design Pattern"]
    title_suffixes = (" Design Pattern",)


class SourceMakingCodeSmellsSpider(SourceMakingSpider):
    name = "sourcemaking-code-smells"
    start_urls = [CODE_SMELLS_URL]
    item_path_prefix = ("refactoring", "smells")
    excluded_item_slugs = SMELL_CATEGORY_SLUGS
    base_tag_names = ["Code Smell"]
    title_suffixes: tuple[str, ...] = ()


class SourceMakingRefactoringsSpider(SourceMakingSpider):
    name = "sourcemaking-refactorings"
    start_urls = [REFACTORINGS_URL]
    item_path_prefix = ("refactoring",)
    excluded_item_slugs = {*REFACTORING_CATEGORY_SLUGS, "smells", "refactorings"}
    base_tag_names = ["Refactoring Technique"]
    title_suffixes: tuple[str, ...] = ()
