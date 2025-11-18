"""
Setup script for news_scraper package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="news_scraper",
    version="1.0.0",
    author="News Scraper Team",
    description="A comprehensive web scraping project using Scrapy for news articles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/news_scraper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "news-scraper=news_scraper.cli:main",
        ],
    },
)
