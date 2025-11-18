"""
Tests for the analyzer module.
"""
import pytest
import sqlite3
import pandas as pd
from pathlib import Path
from news_scraper.analyzer import NewsAnalyzer


@pytest.fixture
def test_db(tmp_path):
    """Create a test database with sample data."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            summary TEXT,
            publication_date TEXT,
            author TEXT,
            url TEXT,
            scraped_at TEXT
        )
    """)
    
    # Insert sample data
    cursor.execute("""
        INSERT INTO articles VALUES
        (1, 'Test Article One', 'This is a test summary about technology', 
         '2024-01-01', 'John Doe', 'http://example.com/1', '2024-01-01'),
        (2, 'Test Article Two', 'Another test about technology and innovation',
         '2024-01-02', 'Jane Smith', 'http://example.com/2', '2024-01-02')
    """)
    
    conn.commit()
    conn.close()
    
    return str(db_path)


def test_analyzer_initialization():
    """Test analyzer initialization."""
    analyzer = NewsAnalyzer("test.db")
    assert analyzer.database_path == "test.db"
    assert analyzer.df is None


def test_load_data(test_db):
    """Test loading data from database."""
    analyzer = NewsAnalyzer(test_db)
    df = analyzer.load_data()
    
    assert df is not None
    assert len(df) == 2
    assert 'title' in df.columns
    assert 'summary' in df.columns


def test_extract_keywords(test_db):
    """Test keyword extraction."""
    analyzer = NewsAnalyzer(test_db)
    analyzer.load_data()
    
    keywords = analyzer.extract_keywords(top_n=5)
    
    assert isinstance(keywords, dict)
    assert 'technology' in keywords
    assert keywords['technology'] == 2


def test_extract_keywords_empty_data():
    """Test keyword extraction with no data."""
    analyzer = NewsAnalyzer("nonexistent.db")
    keywords = analyzer.extract_keywords()
    
    assert keywords == {}


def test_generate_report(test_db, tmp_path):
    """Test CSV report generation."""
    analyzer = NewsAnalyzer(test_db)
    analyzer.load_data()
    
    output_path = tmp_path / "report.csv"
    analyzer.generate_report(str(output_path))
    
    assert output_path.exists()
    
    # Load and verify CSV
    df = pd.read_csv(output_path)
    assert len(df) == 2
    assert 'title_length' in df.columns


def test_get_summary_stats(test_db):
    """Test summary statistics."""
    analyzer = NewsAnalyzer(test_db)
    analyzer.load_data()
    
    stats = analyzer.get_summary_stats()
    
    assert stats['total_articles'] == 2
    assert stats['unique_authors'] == 2
