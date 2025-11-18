"""
BBC News Spider - Scrapes articles from BBC News website.
"""
import scrapy
from datetime import datetime
from news_scraper.items import NewsArticleItem
import re
import logging

logger = logging.getLogger(__name__)


class BBCSpider(scrapy.Spider):
    """
    Spider to scrape BBC News articles.
    Handles pagination and extracts article details.
    """
    name = "bbc"
    allowed_domains = ["bbc.com"]
    
    # Start with multiple news categories
    start_urls = [
        "https://www.bbc.com/news",
        "https://www.bbc.com/news/world",
        "https://www.bbc.com/news/business",
        "https://www.bbc.com/news/technology",
    ]

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 100,  # Limit for demo purposes
    }

    def parse(self, response):
        """
        Parse the main news page and extract article links.
        """
        logger.info(f"Parsing: {response.url}")
        
        # Find all article links
        article_links = response.css('a[href*="/news/"]::attr(href)').getall()
        
        # Filter and deduplicate article links
        seen = set()
        for link in article_links:
            # Clean and validate link
            if not link.startswith('http'):
                link = response.urljoin(link)
            
            # Skip if already seen or not a proper article
            if link in seen or not self._is_article_url(link):
                continue
                
            seen.add(link)
            
            # Follow the article link
            yield scrapy.Request(
                link,
                callback=self.parse_article,
                errback=self.errback_httpbin,
                dont_filter=False
            )
        
        # Handle pagination (if available)
        next_page = response.css('a.qa-pagination-next-page::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            logger.info(f"Following pagination: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        """
        Parse individual article page and extract details.
        """
        logger.debug(f"Parsing article: {response.url}")
        
        # Extract article details
        item = NewsArticleItem()
        
        # Title
        title = response.css('h1::text').get() or response.css('h1 *::text').get()
        if not title:
            title = response.css('title::text').get()
        item['title'] = title.strip() if title else "No Title"
        
        # Summary/Description
        summary = (
            response.css('meta[property="og:description"]::attr(content)').get() or
            response.css('meta[name="description"]::attr(content)').get() or
            response.css('article p::text').get()
        )
        item['summary'] = summary.strip() if summary else "No summary available"
        
        # Publication date
        pub_date = (
            response.css('time::attr(datetime)').get() or
            response.css('meta[property="article:published_time"]::attr(content)').get() or
            response.css('[data-datetime]::attr(data-datetime)').get()
        )
        
        if pub_date:
            item['publication_date'] = pub_date
        else:
            # If no date found, use current date as fallback
            item['publication_date'] = datetime.now().isoformat()
        
        # Author
        author = (
            response.css('meta[property="article:author"]::attr(content)').get() or
            response.css('[rel="author"]::text').get() or
            response.css('.author::text').get() or
            response.css('span[class*="author"]::text').get()
        )
        item['author'] = author.strip() if author else "BBC News"
        
        # URL
        item['url'] = response.url
        
        # Scraped timestamp
        item['scraped_at'] = datetime.now().isoformat()
        
        yield item

    def _is_article_url(self, url):
        """
        Check if URL is likely an article page.
        """
        # Exclude certain patterns that are not articles
        exclude_patterns = [
            '/live/', '/av/', '/video/', '/media/',
            '/programmes/', '/sport/', '/weather/',
            'bbc.co.uk', 'bbc.com/future'
        ]
        
        for pattern in exclude_patterns:
            if pattern in url:
                return False
        
        # Must contain /news/ and have a proper article path
        if '/news/' in url:
            # Check if it has an article ID pattern
            if re.search(r'/news/[a-z-]+-\d+', url):
                return True
        
        return False

    def errback_httpbin(self, failure):
        """
        Handle request errors.
        """
        logger.error(f"Request failed: {failure.request.url}")
        logger.error(f"Error: {failure.value}")
