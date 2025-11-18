"""
Tests for Scrapy pipelines.
"""
import pytest
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from scrapy.http import Response, Request
from scrapy import Spider
from news_scraper.items import NewsArticleItem
from news_scraper.pipelines import DateFilterPipeline, DatabasePipeline


class MockSpider(Spider):
    """Mock spider for testing."""
    name = 'test_spider'


@pytest.fixture
def test_spider():
    """Create a test spider."""
    return MockSpider()


@pytest.fixture
def test_item():
    """Create a test item."""
    item = NewsArticleItem()
    item['title'] = 'Test Article'
    item['summary'] = 'Test summary'
    item['publication_date'] = datetime.now().isoformat()
    item['author'] = 'Test Author'
    item['url'] = 'http://example.com/test'
    item['scraped_at'] = datetime.now().isoformat()
    return item


def test_date_filter_pipeline_recent_article(test_spider, test_item):
    """Test date filter with recent article."""
    pipeline = DateFilterPipeline(days_to_scrape=7)
    
    # Should pass through
    result = pipeline.process_item(test_item, test_spider)
    assert result == test_item


def test_date_filter_pipeline_old_article(test_spider, test_item):
    """Test date filter with old article."""
    pipeline = DateFilterPipeline(days_to_scrape=7)
    
    # Set old date
    test_item['publication_date'] = (datetime.now() - timedelta(days=10)).isoformat()
    
    # Should raise exception
    with pytest.raises(Exception):
        pipeline.process_item(test_item, test_spider)


def test_database_pipeline_create_table(test_spider, tmp_path):
    """Test database table creation."""
    db_path = str(tmp_path / "test.db")
    pipeline = DatabasePipeline(db_path)
    
    pipeline.open_spider(test_spider)
    
    # Check table exists
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles'")
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None
    pipeline.close_spider(test_spider)


def test_database_pipeline_insert_item(test_spider, test_item, tmp_path):
    """Test inserting item into database."""
    db_path = str(tmp_path / "test.db")
    pipeline = DatabasePipeline(db_path)
    
    pipeline.open_spider(test_spider)
    pipeline.process_item(test_item, test_spider)
    pipeline.close_spider(test_spider)
    
    # Verify item was inserted
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE url=?", (test_item['url'],))
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None
    assert result[1] == test_item['title']


def test_database_pipeline_duplicate_url(test_spider, test_item, tmp_path):
    """Test handling duplicate URLs."""
    db_path = str(tmp_path / "test.db")
    pipeline = DatabasePipeline(db_path)
    
    pipeline.open_spider(test_spider)
    pipeline.process_item(test_item, test_spider)
    
    # Try to insert duplicate
    test_item['title'] = 'Updated Title'
    pipeline.process_item(test_item, test_spider)
    pipeline.close_spider(test_spider)
    
    # Verify only one item (replaced)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE url=?", (test_item['url'],))
    count = cursor.fetchone()[0]
    conn.close()
    
    assert count == 1
