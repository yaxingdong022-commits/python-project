"""
Scrapy settings for news_scraper project.
"""

BOT_NAME = "news_scraper"

SPIDER_MODULES = ["news_scraper.spiders"]
NEWSPIDER_MODULE = "news_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    "news_scraper.middlewares.NewsScraperSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "news_scraper.middlewares.UserAgentRotationMiddleware": 400,
    "news_scraper.middlewares.NewsScraperDownloaderMiddleware": 543,
}

# Enable or disable extensions
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    "news_scraper.pipelines.DateFilterPipeline": 100,
    "news_scraper.pipelines.DatabasePipeline": 300,
}

# Enable and configure the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Database settings
DATABASE_PATH = "data/news_articles.db"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "logs/scraper.log"
LOG_ENABLED = True
LOG_ENCODING = "utf-8"
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

# Days to scrape (last 7 days)
DAYS_TO_SCRAPE = 7
