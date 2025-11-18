"""
Tests for Scrapy items.
"""
import pytest
from datetime import datetime
from news_scraper.items import NewsArticleItem


def test_create_item():
    """Test creating a NewsArticleItem."""
    item = NewsArticleItem()
    item['title'] = 'Test Title'
    item['summary'] = 'Test Summary'
    item['publication_date'] = datetime.now().isoformat()
    item['author'] = 'Test Author'
    item['url'] = 'http://example.com'
    item['scraped_at'] = datetime.now().isoformat()
    
    assert item['title'] == 'Test Title'
    assert item['author'] == 'Test Author'


def test_item_repr():
    """Test item string representation."""
    item = NewsArticleItem()
    item['title'] = 'A' * 100
    
    repr_str = repr(item)
    assert '<NewsArticleItem:' in repr_str
    assert len(repr_str) < 100  # Should be truncated


def test_item_fields():
    """Test that all expected fields are available."""
    item = NewsArticleItem()
    
    # Set all fields
    item['title'] = 'Title'
    item['summary'] = 'Summary'
    item['publication_date'] = 'Date'
    item['author'] = 'Author'
    item['url'] = 'URL'
    item['scraped_at'] = 'Time'
    
    assert len(item) == 6
