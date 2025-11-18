"""
Demo script to test the news scraper functionality with sample data.
This creates sample data without hitting real news websites.
"""
import sqlite3
from datetime import datetime, timedelta
import random
from pathlib import Path
from news_scraper.analyzer import NewsAnalyzer
from news_scraper.visualizer import NewsVisualizer


def create_sample_data():
    """Create sample news articles in the database."""
    # Create data directory
    Path("data").mkdir(exist_ok=True)
    
    # Sample data
    sample_articles = [
        {
            "title": "Climate Change Summit Reaches Historic Agreement",
            "summary": "World leaders gather to address climate change with new technology solutions and renewable energy commitments",
            "author": "Jane Smith",
            "date": 0
        },
        {
            "title": "Technology Giants Announce AI Breakthrough",
            "summary": "Major technology companies unveil new artificial intelligence systems with enhanced capabilities",
            "author": "John Doe",
            "date": 1
        },
        {
            "title": "Global Economy Shows Signs of Recovery",
            "summary": "Economic indicators suggest positive growth trends across multiple sectors and markets worldwide",
            "author": "Jane Smith",
            "date": 2
        },
        {
            "title": "Scientists Discover New Treatment for Disease",
            "summary": "Medical researchers announce breakthrough in healthcare technology and treatment methods",
            "author": "Dr. Michael Chen",
            "date": 1
        },
        {
            "title": "Space Exploration Mission Launches Successfully",
            "summary": "Space agency sends new mission to explore distant planets using advanced technology",
            "author": "Sarah Johnson",
            "date": 3
        },
        {
            "title": "Renewable Energy Investment Reaches Record High",
            "summary": "Investment in renewable energy and climate solutions breaks records as demand increases",
            "author": "John Doe",
            "date": 2
        },
        {
            "title": "Education Reform Initiative Announced",
            "summary": "Government unveils new education policies focusing on technology integration and student success",
            "author": "Emma Williams",
            "date": 4
        },
        {
            "title": "Cybersecurity Threats Increase Globally",
            "summary": "Technology experts warn about rising cybersecurity risks and recommend enhanced security measures",
            "author": "Mike Anderson",
            "date": 1
        },
        {
            "title": "International Trade Agreement Finalized",
            "summary": "Multiple countries sign trade agreement covering technology, business, and economic cooperation",
            "author": "Jane Smith",
            "date": 5
        },
        {
            "title": "Healthcare Innovation Shows Promise",
            "summary": "New healthcare technology demonstrates effectiveness in clinical trials with positive outcomes",
            "author": "Dr. Michael Chen",
            "date": 2
        },
        {
            "title": "Transportation Revolution Gains Momentum",
            "summary": "Electric vehicle technology advances as cities invest in sustainable transportation infrastructure",
            "author": "Sarah Johnson",
            "date": 3
        },
        {
            "title": "Financial Markets React to Policy Changes",
            "summary": "Global financial markets respond to new economic policies and business regulations",
            "author": "John Doe",
            "date": 1
        },
        {
            "title": "Artificial Intelligence Ethics Debate Intensifies",
            "summary": "Technology leaders discuss ethical implications of artificial intelligence and automated systems",
            "author": "Emma Williams",
            "date": 4
        },
        {
            "title": "Agricultural Technology Improves Crop Yields",
            "summary": "Farmers adopt new agricultural technology and climate-adapted methods to increase production",
            "author": "Mike Anderson",
            "date": 2
        },
        {
            "title": "Digital Currency Adoption Accelerates",
            "summary": "Financial institutions embrace digital currency technology and blockchain systems",
            "author": "John Doe",
            "date": 3
        },
    ]
    
    # Create database
    db_path = "data/news_articles.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
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
    
    # Insert sample articles
    now = datetime.now()
    for i, article in enumerate(sample_articles):
        pub_date = now - timedelta(days=article["date"])
        url = f"http://example.com/news/article-{i+1}"
        
        cursor.execute("""
            INSERT OR REPLACE INTO articles 
            (title, summary, publication_date, author, url, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            article["title"],
            article["summary"],
            pub_date.isoformat(),
            article["author"],
            url,
            now.isoformat()
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✓ Created sample database with {len(sample_articles)} articles")


def main():
    """Run the demo."""
    print("\n" + "="*60)
    print("  News Scraper Demo")
    print("="*60 + "\n")
    
    # Create sample data
    print("Step 1: Creating sample data...")
    create_sample_data()
    
    # Analyze data
    print("\nStep 2: Analyzing articles...")
    analyzer = NewsAnalyzer("data/news_articles.db")
    df = analyzer.load_data()
    print(f"✓ Loaded {len(df)} articles")
    
    # Extract keywords
    keywords = analyzer.extract_keywords(top_n=20)
    print(f"✓ Extracted {len(keywords)} keywords")
    
    # Generate report
    print("\nStep 3: Generating CSV report...")
    analyzer.generate_report()
    
    # Create visualizations
    print("\nStep 4: Creating visualizations...")
    visualizer = NewsVisualizer("data")
    visualizer.plot_keyword_frequency(keywords)
    visualizer.plot_articles_per_author(df)
    
    print("\n" + "="*60)
    print("  Demo completed successfully!")
    print("  Check the 'data' directory for results:")
    print("    - news_articles.db (SQLite database)")
    print("    - analysis_report.csv (Analysis report)")
    print("    - keyword_frequency.png (Keyword chart)")
    print("    - articles_per_author.png (Author chart)")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
