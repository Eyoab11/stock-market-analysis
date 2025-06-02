"""
Module for analysis operations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from typing import Tuple
import logging

class NewsAnalyzer:
    """Perform exploratory analysis on news data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.logger = logging.getLogger(__name__)
        
    def get_basic_stats(self) -> pd.Series:
        """Compute basic statistics"""
        stats = {
            "total_articles": len(self.df),
            "unique_stocks": self.df['stock'].nunique(),
            "unique_publishers": self.df['publisher'].nunique(),
            "date_range": (self.df['date'].min(), self.df['date'].max()),
            "headline_length_avg": self.df['headline'].str.len().mean(),
            "headline_length_std": self.df['headline'].str.len().std()
        }
        return pd.Series(stats)
        
    def analyze_publishers(self, top_n: int = 10) -> pd.Series:
        """Analyze publisher distribution"""
        return self.df['publisher'].value_counts().head(top_n)
        
    def plot_temporal_distribution(self, save_path: str = None) -> Tuple[pd.Series, pd.Series]:
        """Plot temporal patterns"""
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Daily count
        daily = self.df.resample('D', on='date').size()
        sns.lineplot(x=daily.index, y=daily.values, ax=axes[0])
        axes[0].set_title('Articles Published Per Day')
        
        # Hourly distribution
        hourly = self.df['date_hour'].value_counts().sort_index()
        sns.barplot(x=hourly.index, y=hourly.values, ax=axes[1])
        axes[1].set_title('Article Publication by Hour of Day')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()
            
        return daily, hourly


class SentimentAnalyzer:
    """Perform sentiment analysis on news headlines"""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.logger = logging.getLogger(__name__)
        
    def analyze(self, headlines: pd.Series) -> pd.DataFrame:
        """Analyze sentiment for a series of headlines"""
        results = pd.DataFrame({
            'vader': headlines.apply(lambda x: self.sia.polarity_scores(x)['compound']),
            'textblob': headlines.apply(lambda x: TextBlob(x).sentiment.polarity)
        })
        return results
        
    def plot_sentiment_distribution(self, sentiment_df: pd.DataFrame, save_path: str = None) -> None:
        """Plot sentiment distributions"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        sns.histplot(sentiment_df['vader'], bins=30, ax=axes[0])
        axes[0].set_title('VADER Sentiment Distribution')
        
        sns.histplot(sentiment_df['textblob'], bins=30, ax=axes[1])
        axes[1].set_title('TextBlob Sentiment Distribution')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
            plt.close()


class CorrelationAnalyzer:
    """Analyze correlations between sentiment and stock returns"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_correlation(self, sentiment: pd.Series, returns: pd.Series) -> float:
        """Calculate Pearson correlation between sentiment and returns"""
        aligned_data = pd.concat([sentiment, returns], axis=1).dropna()
        if len(aligned_data) < 2:
            self.logger.warning("Insufficient data for correlation calculation")
            return None
            
        return aligned_data.corr().iloc[0, 1]
        
    def plot_correlation(self, sentiment: pd.Series, returns: pd.Series, save_path: str = None) -> None:
        """Scatter plot of sentiment vs returns"""
        plt.figure(figsize=(10, 6))
        sns.regplot(x=sentiment, y=returns)
        plt.title('Sentiment vs Stock Returns')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Daily Return')
        
        if save_path:
            plt.savefig(save_path)
            plt.close()