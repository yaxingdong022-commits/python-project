"""
Visualization module for news article data.
Uses Matplotlib to create charts and graphs.
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class NewsVisualizer:
    """
    Visualizer for news article data.
    Creates charts and graphs using Matplotlib.
    """

    def __init__(self, output_dir="data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_keyword_frequency(self, keywords, output_file="keyword_frequency.png", top_n=15):
        """
        Create a bar chart of keyword frequencies.
        
        Args:
            keywords: Dictionary of keywords and their frequencies
            output_file: Name of the output file
            top_n: Number of top keywords to display
        """
        if not keywords:
            logger.warning("No keywords to plot")
            return

        try:
            # Sort and get top N keywords
            sorted_keywords = sorted(
                keywords.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:top_n]
            
            words = [k for k, v in sorted_keywords]
            frequencies = [v for k, v in sorted_keywords]

            # Create figure and axis
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create horizontal bar chart
            bars = ax.barh(words, frequencies, color='steelblue')
            
            # Customize the chart
            ax.set_xlabel('Frequency', fontsize=12, fontweight='bold')
            ax.set_ylabel('Keywords', fontsize=12, fontweight='bold')
            ax.set_title('Top Keywords in News Articles', fontsize=14, fontweight='bold')
            ax.invert_yaxis()  # Highest frequency at top
            
            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(
                    width, bar.get_y() + bar.get_height()/2,
                    f' {int(width)}',
                    ha='left', va='center', fontsize=10
                )
            
            # Add grid for better readability
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            
            # Adjust layout
            plt.tight_layout()
            
            # Save figure
            output_path = self.output_dir / output_file
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Keyword frequency chart saved to {output_path}")
            print(f"\n✓ Visualization saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")

    def plot_articles_per_author(self, df, output_file="articles_per_author.png", top_n=10):
        """
        Create a bar chart of articles per author.
        
        Args:
            df: Pandas DataFrame with article data
            output_file: Name of the output file
            top_n: Number of top authors to display
        """
        if df is None or df.empty:
            logger.warning("No data to plot")
            return

        try:
            # Count articles per author
            author_counts = df['author'].value_counts().head(top_n)
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create bar chart
            bars = ax.bar(range(len(author_counts)), author_counts.values, color='coral')
            
            # Customize
            ax.set_xlabel('Author', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Articles', fontsize=12, fontweight='bold')
            ax.set_title('Articles per Author', fontsize=14, fontweight='bold')
            ax.set_xticks(range(len(author_counts)))
            ax.set_xticklabels(author_counts.index, rotation=45, ha='right')
            
            # Add value labels
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10
                )
            
            # Add grid
            ax.grid(axis='y', alpha=0.3, linestyle='--')
            
            # Adjust layout
            plt.tight_layout()
            
            # Save
            output_path = self.output_dir / output_file
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Author chart saved to {output_path}")
            print(f"✓ Author visualization saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating author visualization: {e}")

    def plot_timeline(self, df, output_file="articles_timeline.png"):
        """
        Create a timeline of articles.
        
        Args:
            df: Pandas DataFrame with article data
            output_file: Name of the output file
        """
        if df is None or df.empty:
            logger.warning("No data to plot")
            return

        try:
            # Convert publication_date to datetime
            df['pub_date'] = pd.to_datetime(df['publication_date'], errors='coerce')
            
            # Group by date
            daily_counts = df.groupby(df['pub_date'].dt.date).size()
            
            # Create figure
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Create line plot
            ax.plot(daily_counts.index, daily_counts.values, 
                   marker='o', linewidth=2, markersize=8, color='green')
            
            # Customize
            ax.set_xlabel('Date', fontsize=12, fontweight='bold')
            ax.set_ylabel('Number of Articles', fontsize=12, fontweight='bold')
            ax.set_title('Articles Published Over Time', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, linestyle='--')
            
            # Rotate x-axis labels
            plt.xticks(rotation=45, ha='right')
            
            # Adjust layout
            plt.tight_layout()
            
            # Save
            output_path = self.output_dir / output_file
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Timeline chart saved to {output_path}")
            print(f"✓ Timeline visualization saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating timeline: {e}")


# Import pandas here to avoid circular imports
import pandas as pd
