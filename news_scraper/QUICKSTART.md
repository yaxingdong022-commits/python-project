# Quick Start Guide

Get started with the News Scraper in 5 minutes!

## Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd news_scraper

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Quick Demo

Run the demo to see all features working with sample data:

```bash
python demo.py
```

This will:
- Create a sample database with 15 news articles
- Extract top keywords using NLP
- Generate analysis reports
- Create visualizations

## Try the Real Scraper

### Option 1: Run Everything at Once

```bash
python -m news_scraper.cli run-all
```

### Option 2: Step by Step

```bash
# Step 1: Scrape BBC news (be respectful of rate limits!)
python -m news_scraper.cli scrape --spider bbc --days 7

# Step 2: Analyze the data
python -m news_scraper.cli analyze

# Step 3: Create visualizations
python -m news_scraper.cli visualize
```

## View Results

After running, check the `data/` directory:

```bash
ls -lh data/
# news_articles.db          - SQLite database
# analysis_report.csv       - CSV with statistics
# keyword_frequency.png     - Keyword visualization
# articles_per_author.png   - Author statistics
```

## Run Tests

```bash
pytest -v
```

## Need Help?

```bash
python -m news_scraper.cli --help
python -m news_scraper.cli scrape --help
```

## Common Commands

```bash
# Scrape with custom parameters
python -m news_scraper.cli scrape --spider bbc --days 14

# Extract more keywords
python -m news_scraper.cli analyze --top-keywords 30

# Custom output directory
python -m news_scraper.cli visualize --output-dir ./output
```

## Tips

1. **Respect Rate Limits**: The scraper includes delays and user-agent rotation
2. **Check Logs**: View `logs/scraper.log` for detailed information
3. **Database**: Use any SQLite browser to explore `data/news_articles.db`
4. **Customize**: Edit `news_scraper/settings.py` for configuration

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Add support for more news sources
- Customize the analysis parameters
- Integrate with your own projects

Happy scraping! 🚀
