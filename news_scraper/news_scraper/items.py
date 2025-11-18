"""
Define item models for scraped data.
"""
import scrapy
from datetime import datetime


class NewsArticleItem(scrapy.Item):
    """
    Item model for news articles.
    """
    title = scrapy.Field()
    summary = scrapy.Field()
    publication_date = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    scraped_at = scrapy.Field()
    
    def __repr__(self):
        return f"<NewsArticleItem: {self.get('title', 'N/A')[:50]}>"
