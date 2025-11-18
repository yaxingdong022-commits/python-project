"""
Custom middleware for the news scraper.
"""
from scrapy import signals
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)


class NewsScraperSpiderMiddleware:
    """
    Spider middleware for processing spider input/output.
    """

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        logger.error(f"Spider exception on {response.url}: {exception}")

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        logger.info(f"Spider opened: {spider.name}")


class NewsScraperDownloaderMiddleware:
    """
    Downloader middleware for processing requests/responses.
    """

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        logger.error(f"Downloader exception on {request.url}: {exception}")

    def spider_opened(self, spider):
        logger.info(f"Spider opened: {spider.name}")


class UserAgentRotationMiddleware:
    """
    Middleware to rotate user agents to avoid being banned.
    """

    def __init__(self):
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        try:
            request.headers["User-Agent"] = self.ua.random
            logger.debug(f"Using User-Agent: {request.headers['User-Agent']}")
        except Exception as e:
            logger.warning(f"Failed to set User-Agent: {e}")
        return None
