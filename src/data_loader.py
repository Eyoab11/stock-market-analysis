"""
Module for data loading operations
"""

import pandas as pd
from datetime import datetime
import logging
from typing import Union

class NewsDataLoader:
    """Load and preprocess financial news data"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)
        
    def load(self) -> pd.DataFrame:
        """Load news data from CSV"""
        try:
            df = pd.read_csv(self.filepath, parse_dates=['date'])
            self._preprocess(df)
            self.logger.info(f"Successfully loaded {len(df)} news records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load data: {str(e)}")
            raise
            
    def _preprocess(self, df: pd.DataFrame) -> None:
        """Internal preprocessing"""
        # Clean text fields
        df['headline'] = df['headline'].str.strip()
        df['publisher'] = df['publisher'].str.strip()
        
        # Extract temporal features
        df['date_day'] = df['date'].dt.date
        df['date_hour'] = df['date'].dt.hour
        df['date_weekday'] = df['date'].dt.weekday


class StockDataLoader:
    """Load and preprocess stock price data"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)
        
    def load(self) -> pd.DataFrame:
        """Load stock data from CSV"""
        try:
            df = pd.read_csv(
                self.filepath,
                parse_dates=['date'],
                usecols=['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']
            )
            self._preprocess(df)
            self.logger.info(f"Successfully loaded {len(df)} stock records")
            return df
        except Exception as e:
            self.logger.error(f"Failed to load data: {str(e)}")
            raise
            
    def _preprocess(self, df: pd.DataFrame) -> None:
        """Internal preprocessing"""
        # Ensure numeric columns are properly typed
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Calculate daily returns
        df['daily_return'] = df['close'].pct_change()