# src/data_loader.py

import pandas as pd
import logging

class NewsDataLoader:
    """Load and preprocess financial news data"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)
        
    def load(self) -> pd.DataFrame:
        """Load news data from CSV and perform initial date parsing."""
        self.logger.info(f"Attempting to load news data from: {self.filepath}")
        print(f"DEBUG: [NewsDataLoader.load] Attempting to load: {self.filepath}")
        try:
            # Step 1: Load the CSV without any initial date parsing by read_csv
            df = pd.read_csv(self.filepath)
            self.logger.info(f"CSV loaded. Columns: {df.columns.tolist()}")
            print(f"DEBUG: [NewsDataLoader.load] CSV loaded. Columns: {df.columns.tolist()}")
            
            # Step 2: Check if 'date' column exists
            if 'date' not in df.columns:
                self.logger.error(f"CRITICAL: 'date' column not found in CSV: {self.filepath}. Available columns: {df.columns.tolist()}")
                print(f"DEBUG: [NewsDataLoader.load] CRITICAL: 'date' column MISSING. Available: {df.columns.tolist()}")
                raise KeyError(f"'date' column not found in {self.filepath}. Check CSV header and column names.")

            self.logger.info(f"Initial 'date' column dtype before any conversion: {df['date'].dtype}")
            print(f"DEBUG: [NewsDataLoader.load] Initial 'date' column dtype: {df['date'].dtype}")
            if not df.empty:
                self.logger.info(f"First 5 values of 'date' column (raw): {df['date'].head().tolist()}")
                print(f"DEBUG: [NewsDataLoader.load] First 5 'date' values (raw): {df['date'].head().tolist()}")

            # Step 3: Explicitly convert 'date' column to datetime objects
            self.logger.info(f"Attempting explicit pd.to_datetime on 'date' column (current dtype: {df['date'].dtype})")
            print(f"DEBUG: [NewsDataLoader.load] Attempting explicit pd.to_datetime on 'date' column.")
            
            original_date_series = df['date'].copy() # Keep a copy for comparison if needed
            df['date'] = pd.to_datetime(original_date_series, errors='coerce')
            
            self.logger.info(f"After explicit pd.to_datetime, 'date' column dtype: {df['date'].dtype}")
            print(f"DEBUG: [NewsDataLoader.load] After explicit pd.to_datetime, 'date' column dtype: {df['date'].dtype}")

            if not df.empty:
                self.logger.info(f"First 5 values of 'date' column (after parse): {df['date'].head().tolist()}")
                print(f"DEBUG: [NewsDataLoader.load] First 5 'date' values (after parse): {df['date'].head().tolist()}")

            # Step 4: Verify conversion
            if not pd.api.types.is_datetime64_any_dtype(df['date']):
                self.logger.error(
                    f"CRITICAL FAILURE: 'date' column (dtype: {df['date'].dtype}) DID NOT CONVERT to datetime. "
                    f"Sample values (original): {original_date_series.head().tolist() if not original_date_series.empty else 'N/A'}. "
                    f"This means pandas could not interpret any of the date strings."
                )
                print(
                    f"DEBUG: [NewsDataLoader.load] CRITICAL FAILURE: 'date' column (dtype: {df['date'].dtype}) "
                    f"DID NOT CONVERT to datetime."
                )
                raise TypeError(
                    f"The 'date' column could not be converted to a datetime format. Last known dtype: {df['date'].dtype}. "
                    f"Inspect the CSV file's 'date' column for highly irregular formats or non-date data."
                )

            if df['date'].isnull().all() and not df.empty:
                self.logger.warning(
                    f"WARNING: All date entries in '{self.filepath}' resulted in NaT (Not a Time) after parsing. "
                    f"The 'date' column likely does not contain any valid date strings recognizable by pandas."
                )
                print(f"DEBUG: [NewsDataLoader.load] WARNING: All 'date' entries are NaT.")


            # Step 5: Call _preprocess
            self._preprocess(df)
            self.logger.info(f"Successfully loaded and preprocessed {len(df)} news records from {self.filepath}")
            print(f"DEBUG: [NewsDataLoader.load] Load and preprocess successful.")
            return df
        except FileNotFoundError:
            self.logger.error(f"File not found: {self.filepath}")
            print(f"DEBUG: [NewsDataLoader.load] FileNotFoundError: {self.filepath}")
            raise
        except KeyError as e:
            self.logger.error(f"A required column is missing: {str(e)}")
            print(f"DEBUG: [NewsDataLoader.load] KeyError: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to load or preprocess data from {self.filepath}: {str(e)}", exc_info=True)
            print(f"DEBUG: [NewsDataLoader.load] Exception: {str(e)}")
            raise
            
    def _preprocess(self, df: pd.DataFrame) -> None:
        """Internal preprocessing. Assumes 'date' column is already datetime64."""
        self.logger.info("Starting preprocessing of news data...")
        print("DEBUG: [NewsDataLoader._preprocess] Starting.")

        # --- Date Handling Verification (should be redundant now but good for sanity) ---
        if 'date' not in df.columns:
            self.logger.error("CRITICAL error: 'date' column missing at the start of _preprocess.")
            print("DEBUG: [NewsDataLoader._preprocess] CRITICAL: 'date' column missing.")
            raise KeyError("'date' column is missing and required for preprocessing.")

        self.logger.info(f"Inside _preprocess, 'date' column dtype IS: {df['date'].dtype}")
        print(f"DEBUG: [NewsDataLoader._preprocess] 'date' column dtype: {df['date'].dtype}")
        
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            # This case should ideally not be reached if 'load' method works correctly
            self.logger.error(f"CRITICAL: 'date' column is NOT datetime (is {df['date'].dtype}) in _preprocess. Conversion in 'load' failed.")
            print(f"DEBUG: [NewsDataLoader._preprocess] CRITICAL: 'date' column not datetime, dtype: {df['date'].dtype}")
            raise TypeError(f"Date column not properly converted before _preprocess. Dtype: {df['date'].dtype}")
        
        # --- Clean text fields ---
        if 'headline' in df.columns:
            df['headline'] = df['headline'].astype(str).str.strip()
        if 'publisher' in df.columns:
            df['publisher'] = df['publisher'].astype(str).str.strip()

        # --- Extract temporal features ---
        self.logger.info("Attempting to extract temporal features (date_day, date_hour, date_weekday)...")
        print(f"DEBUG: [NewsDataLoader._preprocess] Attempting .dt access. df['date'].dtype is {df['date'].dtype}")
        if not df.empty:
            print(f"DEBUG: [NewsDataLoader._preprocess] df['date'].head() before .dt:\n{df['date'].head()}")
        
        # This is the line that was failing
        df['date_day'] = df['date'].dt.date 
        df['date_hour'] = df['date'].dt.hour
        df['date_weekday'] = df['date'].dt.weekday
        
        self.logger.info("Temporal features extracted successfully.")
        print("DEBUG: [NewsDataLoader._preprocess] Temporal features extracted.")
        self.logger.info("Preprocessing of news data finished.")
        print("DEBUG: [NewsDataLoader._preprocess] Finished.")

# Keep StockDataLoader as it was or apply similar robust measures if you use it.
# The current error is within NewsDataLoader.
class StockDataLoader:
    # (Keep your existing StockDataLoader code or the last version provided for it)
    # For brevity, I'm not repeating it here, assuming the focus is on NewsDataLoader.
    # If you need it updated too, let me know.
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)
    def load(self): # Placeholder
        self.logger.info(f"StockDataLoader for {self.filepath} - load not fully implemented in this snippet.")
        pass 
    def _preprocess(self, df): # Placeholder
        pass