"""
Utility functions for financial news analysis
"""

import logging
from datetime import datetime
from typing import Tuple
import pandas as pd

def setup_logging(log_file: str = 'analysis.log') -> None:
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def validate_date_range(start_date: str, end_date: str) -> Tuple[datetime, datetime]:
    """Validate and parse date range"""
    try:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        
        if start > end:
            raise ValueError("Start date must be before end date")
            
        return start, end
    except Exception as e:
        raise ValueError(f"Invalid date range: {str(e)}")