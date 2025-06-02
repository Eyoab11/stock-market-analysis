"""
financial-news-analysis core package

Exposes main classes and functions for financial news analysis
"""

# Import core classes to make them available at package level
from .data_loader import NewsDataLoader, StockDataLoader
from .analyzer import NewsAnalyzer, SentimentAnalyzer, CorrelationAnalyzer
from .utils import setup_logging, validate_date_range

# Package version
__version__ = "0.1.0"

# Expose these when importing from package
__all__ = [
    'NewsDataLoader',
    'StockDataLoader',
    'NewsAnalyzer',
    'SentimentAnalyzer',
    'CorrelationAnalyzer',
    'setup_logging',
    'validate_date_range'
]