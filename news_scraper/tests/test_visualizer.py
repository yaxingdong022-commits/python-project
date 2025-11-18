"""
Tests for the visualizer module.
"""
import pytest
import pandas as pd
from pathlib import Path
from news_scraper.visualizer import NewsVisualizer


@pytest.fixture
def test_keywords():
    """Sample keywords for testing."""
    return {
        'technology': 10,
        'business': 8,
        'politics': 6,
        'climate': 5,
        'economy': 4
    }


@pytest.fixture
def test_dataframe():
    """Sample dataframe for testing."""
    data = {
        'title': ['Article 1', 'Article 2', 'Article 3'],
        'summary': ['Summary 1', 'Summary 2', 'Summary 3'],
        'author': ['Author A', 'Author B', 'Author A'],
        'publication_date': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'url': ['url1', 'url2', 'url3'],
        'scraped_at': ['2024-01-01', '2024-01-02', '2024-01-03']
    }
    return pd.DataFrame(data)


def test_visualizer_initialization(tmp_path):
    """Test visualizer initialization."""
    viz = NewsVisualizer(str(tmp_path))
    assert viz.output_dir == tmp_path
    assert viz.output_dir.exists()


def test_plot_keyword_frequency(test_keywords, tmp_path):
    """Test keyword frequency plot creation."""
    viz = NewsVisualizer(str(tmp_path))
    output_file = "test_keywords.png"
    
    viz.plot_keyword_frequency(test_keywords, output_file)
    
    output_path = tmp_path / output_file
    assert output_path.exists()


def test_plot_keyword_frequency_empty(tmp_path):
    """Test plotting with no keywords."""
    viz = NewsVisualizer(str(tmp_path))
    # Should not raise exception
    viz.plot_keyword_frequency({}, "empty.png")


def test_plot_articles_per_author(test_dataframe, tmp_path):
    """Test articles per author plot."""
    viz = NewsVisualizer(str(tmp_path))
    output_file = "test_authors.png"
    
    viz.plot_articles_per_author(test_dataframe, output_file)
    
    output_path = tmp_path / output_file
    assert output_path.exists()


def test_plot_articles_per_author_empty(tmp_path):
    """Test plotting with empty dataframe."""
    viz = NewsVisualizer(str(tmp_path))
    empty_df = pd.DataFrame()
    
    # Should not raise exception
    viz.plot_articles_per_author(empty_df, "empty.png")
