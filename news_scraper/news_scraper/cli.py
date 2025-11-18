"""
Command-line interface for the news scraper.
"""
import argparse
import sys
import logging
from pathlib import Path
import asyncio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_scraper.analyzer import NewsAnalyzer
from news_scraper.visualizer import NewsVisualizer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class NewsCLI:
    """Command-line interface for news scraper."""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self):
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            description="News Scraper - Scrape and analyze news articles",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Scrape BBC news
  python -m news_scraper.cli scrape --spider bbc
  
  # Analyze scraped data
  python -m news_scraper.cli analyze
  
  # Visualize keywords
  python -m news_scraper.cli visualize
  
  # Run full pipeline
  python -m news_scraper.cli run-all
            """
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Scrape command
        scrape_parser = subparsers.add_parser('scrape', help='Scrape news articles')
        scrape_parser.add_argument(
            '--spider', 
            type=str, 
            default='bbc',
            choices=['bbc'],
            help='Spider to use for scraping'
        )
        scrape_parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to scrape (default: 7)'
        )

        # Analyze command
        analyze_parser = subparsers.add_parser('analyze', help='Analyze scraped articles')
        analyze_parser.add_argument(
            '--database',
            type=str,
            default='data/news_articles.db',
            help='Path to database file'
        )
        analyze_parser.add_argument(
            '--top-keywords',
            type=int,
            default=20,
            help='Number of top keywords to extract'
        )

        # Visualize command
        visualize_parser = subparsers.add_parser('visualize', help='Visualize analysis results')
        visualize_parser.add_argument(
            '--database',
            type=str,
            default='data/news_articles.db',
            help='Path to database file'
        )
        visualize_parser.add_argument(
            '--output-dir',
            type=str,
            default='data',
            help='Directory for output files'
        )

        # Run all command
        run_all_parser = subparsers.add_parser('run-all', help='Run complete pipeline')
        run_all_parser.add_argument(
            '--spider',
            type=str,
            default='bbc',
            choices=['bbc'],
            help='Spider to use'
        )
        run_all_parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to scrape'
        )

        return parser

    def scrape(self, args):
        """Run the scraper."""
        print(f"\n{'='*60}")
        print(f"  Starting {args.spider.upper()} News Scraper")
        print(f"  Scraping articles from the last {args.days} days")
        print(f"{'='*60}\n")

        try:
            # Create logs directory
            Path('logs').mkdir(exist_ok=True)
            
            # Get Scrapy settings
            settings = get_project_settings()
            settings['DAYS_TO_SCRAPE'] = args.days
            
            # Create crawler process
            process = CrawlerProcess(settings)
            
            # Add spider
            if args.spider == 'bbc':
                from news_scraper.spiders.bbc_spider import BBCSpider
                process.crawl(BBCSpider)
            
            # Start scraping
            process.start()
            
            print(f"\n{'='*60}")
            print("  ✓ Scraping completed successfully!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            sys.exit(1)

    def analyze(self, args):
        """Analyze scraped articles."""
        print(f"\n{'='*60}")
        print("  Analyzing Scraped Articles")
        print(f"{'='*60}\n")

        try:
            analyzer = NewsAnalyzer(args.database)
            
            # Load data
            df = analyzer.load_data()
            if df.empty:
                print("⚠ No data found in database. Please run scraping first.")
                return
            
            # Extract keywords
            keywords = analyzer.extract_keywords(top_n=args.top_keywords)
            
            # Generate report
            analyzer.generate_report()
            
            # Print top keywords
            print("\n=== Top Keywords ===")
            for i, (word, freq) in enumerate(sorted(
                keywords.items(), key=lambda x: x[1], reverse=True
            )[:10], 1):
                print(f"{i:2d}. {word:20s} - {freq:3d} occurrences")
            
            print(f"\n{'='*60}")
            print("  ✓ Analysis completed successfully!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            sys.exit(1)

    def visualize(self, args):
        """Create visualizations."""
        print(f"\n{'='*60}")
        print("  Creating Visualizations")
        print(f"{'='*60}\n")

        try:
            # Analyze data
            analyzer = NewsAnalyzer(args.database)
            df = analyzer.load_data()
            
            if df.empty:
                print("⚠ No data found in database. Please run scraping first.")
                return
            
            keywords = analyzer.extract_keywords(top_n=20)
            
            # Create visualizations
            visualizer = NewsVisualizer(args.output_dir)
            visualizer.plot_keyword_frequency(keywords)
            visualizer.plot_articles_per_author(df)
            
            print(f"\n{'='*60}")
            print("  ✓ Visualizations created successfully!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            logger.error(f"Visualization failed: {e}")
            sys.exit(1)

    def run_all(self, args):
        """Run complete pipeline."""
        print(f"\n{'='*60}")
        print("  Running Complete News Scraping Pipeline")
        print(f"{'='*60}\n")

        # Run scraping
        self.scrape(args)
        
        # Create analysis args
        analyze_args = argparse.Namespace(
            database='data/news_articles.db',
            top_keywords=20
        )
        self.analyze(analyze_args)
        
        # Create visualization args
        visualize_args = argparse.Namespace(
            database='data/news_articles.db',
            output_dir='data'
        )
        self.visualize(visualize_args)
        
        print(f"\n{'='*60}")
        print("  ✓ Complete pipeline finished successfully!")
        print(f"  Check the 'data' directory for results")
        print(f"{'='*60}\n")

    def run(self):
        """Run the CLI."""
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return
        
        # Route to appropriate command
        if args.command == 'scrape':
            self.scrape(args)
        elif args.command == 'analyze':
            self.analyze(args)
        elif args.command == 'visualize':
            self.visualize(args)
        elif args.command == 'run-all':
            self.run_all(args)


def main():
    """Entry point for CLI."""
    cli = NewsCLI()
    cli.run()


if __name__ == '__main__':
    main()
