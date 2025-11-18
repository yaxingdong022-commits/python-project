# Python Projects Repository

This repository contains various Python practice projects and a comprehensive web scraping project.

## Featured Project: News Scraper

### 🚀 Comprehensive Web Scraping Project with Scrapy

A production-ready web scraping application built with Python 3.12 and the Scrapy framework.

**Location**: `news_scraper/`

#### Key Features
- 📰 Scrapes news articles from BBC News
- 🗄️ SQLite database for data persistence
- 📊 Data analysis with Pandas
- 🔤 NLP keyword extraction using NLTK
- 📈 Matplotlib visualizations
- 🖥️ User-friendly CLI tool
- ✅ 19 passing tests with pytest
- 📚 Comprehensive documentation

#### Quick Start

```bash
cd news_scraper

# Run demo with sample data
python demo.py

# Or use the full scraper
python -m news_scraper.cli run-all
```

#### Documentation
- 📖 [Full README](news_scraper/README.md) - Complete documentation
- ⚡ [Quick Start Guide](news_scraper/QUICKSTART.md) - Get started in 5 minutes
- 🔧 [Technical Features](news_scraper/FEATURES.md) - Deep dive into implementation
- 📋 [Project Summary](news_scraper/PROJECT_SUMMARY.md) - Overview and statistics

#### What You Get
- **Web Scraping**: Scrapy-based spider with pagination and anti-ban features
- **Data Storage**: SQLite database with proper schema design
- **Data Analysis**: Pandas-powered analysis with keyword extraction
- **Visualizations**: Professional charts showing keyword frequency and trends
- **CLI Tool**: Easy-to-use command-line interface
- **Testing**: Comprehensive test suite with 100% pass rate
- **Documentation**: Extensive guides and examples

#### Technologies Used
- Python 3.12 (async support)
- Scrapy 2.11+
- Pandas 2.1+
- NLTK 3.8+
- Matplotlib 3.8+
- pytest 7.4+
- SQLite

#### Sample Output

The scraper generates:
1. **SQLite Database** - All scraped articles
2. **CSV Report** - Detailed analysis with statistics
3. **Visualizations** - Keyword frequency and author charts
4. **Logs** - Comprehensive logging for debugging

#### Test Results
```
19 passed in 1.74s ✅
```

#### Security
- Zero vulnerabilities (CodeQL verified) ✅
- SQL injection protection ✅
- Input validation ✅
- Proper error handling ✅

---

## Other Projects

This repository also contains various Python practice exercises in the `python实战练习/` directory.

## Contributing

Feel free to explore, use, and contribute to these projects!

## License

Educational and practice purposes.
