from pathlib import Path

BOT_NAME = "modwire_scrapers"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE_ROOT = PROJECT_ROOT / ".scrapy"

SPIDER_MODULES = ["modwire.apps.scrapers.spiders"]
NEWSPIDER_MODULE = "modwire.apps.scrapers.spiders"

ADDONS = {}

USER_AGENT = "ModwireRecordsBot/0.1"

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

COOKIES_ENABLED = False

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = str(CACHE_ROOT / "httpcache")
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

FEED_EXPORT_ENCODING = "utf-8"
