"""
Item pipelines for processing scraped data.
"""
import sqlite3
import logging
from datetime import datetime, timedelta
from itemadapter import ItemAdapter
from pathlib import Path

logger = logging.getLogger(__name__)


class DateFilterPipeline:
    """
    Pipeline to filter articles by publication date (last 7 days).
    """

    def __init__(self, days_to_scrape):
        self.days_to_scrape = days_to_scrape
        self.cutoff_date = datetime.now() - timedelta(days=days_to_scrape)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            days_to_scrape=crawler.settings.get("DAYS_TO_SCRAPE", 7)
        )

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Check if publication_date exists
        if not adapter.get("publication_date"):
            logger.warning("Article has no publication date, skipping")
            raise Exception("No publication date")
        
        try:
            # Parse publication date
            pub_date = adapter.get("publication_date")
            if isinstance(pub_date, str):
                # Try to parse string date
                try:
                    pub_date = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                except ValueError:
                    # Try alternative formats
                    for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d %B %Y"]:
                        try:
                            pub_date = datetime.strptime(pub_date, fmt)
                            break
                        except ValueError:
                            continue
            
            # Check if article is within date range
            if isinstance(pub_date, datetime):
                if pub_date < self.cutoff_date:
                    logger.info(f"Article too old: {adapter.get('title')[:50]}")
                    raise Exception("Article too old")
            else:
                logger.warning(f"Could not parse date: {adapter.get('publication_date')}")
                
        except Exception as e:
            logger.debug(f"Date filtering error: {e}")
            # Allow through if we can't parse the date
            pass
        
        return item


class DatabasePipeline:
    """
    Pipeline to store items in SQLite database.
    """

    def __init__(self, database_path):
        self.database_path = database_path
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_path=crawler.settings.get("DATABASE_PATH", "data/news_articles.db")
        )

    def open_spider(self, spider):
        """Initialize database connection and create table."""
        # Create data directory if it doesn't exist
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()
        
        # Create table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT,
                publication_date TEXT,
                author TEXT,
                url TEXT UNIQUE,
                scraped_at TEXT NOT NULL
            )
        """)
        self.conn.commit()
        logger.info(f"Database initialized at {self.database_path}")

    def close_spider(self, spider):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")

    def process_item(self, item, spider):
        """Insert item into database."""
        adapter = ItemAdapter(item)
        
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO articles 
                (title, summary, publication_date, author, url, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                adapter.get("title"),
                adapter.get("summary"),
                str(adapter.get("publication_date")),
                adapter.get("author"),
                adapter.get("url"),
                adapter.get("scraped_at", datetime.now().isoformat())
            ))
            self.conn.commit()
            logger.debug(f"Saved article: {adapter.get('title')[:50]}")
        except sqlite3.IntegrityError:
            logger.debug(f"Article already exists: {adapter.get('url')}")
        except Exception as e:
            logger.error(f"Error saving article: {e}")
        
        return item
