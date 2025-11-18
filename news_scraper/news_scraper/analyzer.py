"""
Data analysis module for news articles.
Uses Pandas for data manipulation and NLTK for NLP.
"""
import sqlite3
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import logging
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """
    Analyzer for news articles data.
    Performs keyword extraction and analysis.
    """

    def __init__(self, database_path="data/news_articles.db"):
        self.database_path = database_path
        self.df = None
        self._ensure_nltk_data()

    def _ensure_nltk_data(self):
        """Download required NLTK data if not present."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            logger.info("Downloading NLTK punkt_tab tokenizer...")
            nltk.download('punkt_tab', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            logger.info("Downloading NLTK stopwords...")
            nltk.download('stopwords', quiet=True)

    def load_data(self):
        """Load data from SQLite database into pandas DataFrame."""
        try:
            conn = sqlite3.connect(self.database_path)
            self.df = pd.read_sql_query("SELECT * FROM articles", conn)
            conn.close()
            logger.info(f"Loaded {len(self.df)} articles from database")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return pd.DataFrame()

    def extract_keywords(self, top_n=20):
        """
        Extract top keywords from article titles and summaries.
        
        Args:
            top_n: Number of top keywords to return
            
        Returns:
            Dictionary of keywords and their frequencies
        """
        if self.df is None or self.df.empty:
            logger.warning("No data loaded")
            return {}

        # Combine title and summary for analysis
        text_data = (
            self.df['title'].fillna('') + ' ' + 
            self.df['summary'].fillna('')
        ).str.lower()

        # Get English stopwords
        stop_words = set(stopwords.words('english'))
        
        # Add custom stopwords relevant to news
        custom_stopwords = {
            'said', 'says', 'bbc', 'news', 'article', 'video',
            'mr', 'ms', 'mrs', 'dr', 'would', 'could', 'also',
            'new', 'one', 'two', 'three', 'many', 'first',
            'last', 'may', 'de', 'la', 'el'
        }
        stop_words.update(custom_stopwords)

        # Tokenize and filter
        all_words = []
        for text in text_data:
            # Remove special characters and numbers
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            
            # Tokenize
            try:
                words = word_tokenize(text)
            except Exception as e:
                logger.warning(f"Tokenization error: {e}")
                words = text.split()
            
            # Filter words
            words = [
                word for word in words 
                if word not in stop_words 
                and len(word) > 3
                and word.isalpha()
            ]
            all_words.extend(words)

        # Count frequencies
        word_freq = Counter(all_words)
        top_keywords = dict(word_freq.most_common(top_n))
        
        logger.info(f"Extracted {len(top_keywords)} top keywords")
        return top_keywords

    def generate_report(self, output_path="data/analysis_report.csv"):
        """
        Generate a CSV report with article data and statistics.
        
        Args:
            output_path: Path to save the CSV report
        """
        if self.df is None or self.df.empty:
            logger.warning("No data to generate report")
            return

        try:
            # Create output directory if needed
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Add some analysis columns
            self.df['title_length'] = self.df['title'].str.len()
            self.df['summary_length'] = self.df['summary'].str.len()
            
            # Save to CSV
            self.df.to_csv(output_path, index=False, encoding='utf-8')
            logger.info(f"Report saved to {output_path}")
            
            # Print summary statistics
            print("\n=== Article Statistics ===")
            print(f"Total articles: {len(self.df)}")
            print(f"Average title length: {self.df['title_length'].mean():.2f}")
            print(f"Average summary length: {self.df['summary_length'].mean():.2f}")
            print(f"\nTop authors:")
            print(self.df['author'].value_counts().head())
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")

    def get_summary_stats(self):
        """Get summary statistics of the dataset."""
        if self.df is None or self.df.empty:
            return {}
        
        return {
            'total_articles': len(self.df),
            'unique_authors': self.df['author'].nunique(),
            'date_range': (
                self.df['publication_date'].min(),
                self.df['publication_date'].max()
            ),
        }
