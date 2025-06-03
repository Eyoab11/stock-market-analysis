# Predicting Stock Price Moves with News Sentiment (B5W1 Challenge)

This project, part of the B5W1 Challenge by Nova Financial Solutions, focuses on analyzing a large corpus of financial news data to discover correlations between news sentiment and stock market movements. It involves Data Engineering (DE), Financial Analytics (FA), and Machine Learning Engineering (MLE) skills.

## Business Objective

Nova Financial Solutions aims to enhance its predictive analytics capabilities to significantly boost its financial forecasting accuracy and operational efficiency through advanced data analysis. This project involves:

1.  **Sentiment Analysis:** Performing sentiment analysis on financial news headlines to quantify their tone and associate sentiment scores with respective stock symbols.
2.  **Correlation Analysis:** Establishing statistical correlations between derived news sentiment and corresponding stock price movements, considering publication dates.
3.  **Investment Strategy Recommendations:** Leveraging insights to suggest investment strategies based on the relationship between news sentiment and stock price fluctuations.

## Dataset Overview

**FNSPID (Financial News and Stock Price Integration Dataset)** is used, combining quantitative and qualitative data.

*   **`headline`**: The title of the news article.
*   **`url`**: Direct link to the full news article.
*   **`publisher`**: Author/creator of the article.
*   **`date`**: Publication date and time (UTC-4 timezone).
*   **`stock`**: Stock ticker symbol (e.g., AAPL).

Additionally, historical stock price data (Open, High, Low, Close, Volume) for selected tickers is used, typically sourced from CSV files (e.g., from Yahoo Finance).

## Project Structure

├── .github/
│ └── workflows/
│ └── unittests.yml # (Assumed for CI/CD)
├── .gitignore
├── .vscode/
│ └── settings.json
├── data/ # Raw and processed data
│ ├── raw_analyst_ratings.csv
│ ├── AAPL_historical_data.csv
│ ├── ... (other stock csvs)
│ ├── processed_news_data.pkl
│ ├── AAPL_processed.pkl
│ ├── AAPL_indicators.pkl
│ ├── ... (other processed stock pkls)
│ └── correlation_results.csv
├── notebooks/ # Jupyter notebooks for experimentation
│ ├── eda.ipynb
│ ├── Quantitative-analysis.ipynb
│ ├── News-stock-correlation.ipynb
│ ├── init.py
│ └── README.md
├── plots/ # Plots from Task 1 (EDA)
│ ├── headline_length_distribution.png
│ ├── ...
├── Plots-task2/ # Plots from Task 2 (Technical Indicators)
│ ├── AAPL_sma.png
│ ├── ...
├── Plots-task3/ # Plots from Task 3 (Correlation Analysis)
│ ├── AAPL_sentiment_vs_returns.png
│ ├── ...
├── requirements.txt
├── README.md
├── scripts/ # Standalone scripts for tasks
│ ├── init.py
│ └── README.md
├── src/ # Source code for reusable modules/classes
│ ├── init.py
└── tests/ # Unit test
└── init.py



## Tasks Accomplished

### Task 1: Exploratory Data Analysis (EDA) & Data Preprocessing

*   **Objective:** Understand the financial news dataset, perform EDA, and prepare data for further analysis.
*   **Key Activities:**
    *   Loaded raw news data (`raw_analyst_ratings.csv`).
    *   Performed descriptive statistics: headline length distribution.
    *   Analyzed publisher activity: identified top publishers and publisher domains.
    *   Analyzed publication trends over time (daily and hourly distributions, spike identification).
    *   Conducted basic text analysis: tokenized headlines, removed stopwords, and identified common keywords.
    *   Cleaned and preprocessed news data (handling dates, extracting domains) and saved it as `data/processed_news_data.pkl`.
*   **Outputs:**
    *   Visualizations saved in the `plots/` directory (e.g., `headline_length_distribution.png`, `publisher_distribution.png`).
    *   Processed news data: `data/processed_news_data.pkl`.
*   **notebooks:** `notebooks/eda.ipynb` (or similar)

### Task 2: Quantitative Analysis using TA-Lib

*   **Objective:** Calculate and visualize technical indicators for selected stock symbols.
*   **Key Activities:**
    *   Loaded historical stock price data (OHLCV) for symbols: `TSLA`, `NVDA`, `META`, `AMZN`, `GOOG`, `AAPL`, `MSFT`.
    *   Preprocessed stock data: handled date columns, standardized OHLCV column names, ensured numeric types, and saved processed data (e.g., `data/TSLA_processed.pkl`).
    *   Calculated technical indicators using TA-Lib:
        *   Simple Moving Average (SMA_20)
        *   Relative Strength Index (RSI_14)
        *   Moving Average Convergence Divergence (MACD, MACD_Signal, MACD_Hist)
    *   Saved stock data with calculated indicators (e.g., `data/TSLA_indicators.pkl`).
    *   Visualized stock prices alongside their technical indicators.
*   **Outputs:**
    *   Visualizations saved in the `Plots-task2/` directory (e.g., `TSLA_sma.png`, `TSLA_rsi.png`, `TSLA_macd.png`).
    *   Processed stock data with indicators: `data/{SYMBOL}_indicators.pkl`.
*   **notebooks:** `notebooks/Quantitative-analysis.ipynb` 

### Task 3: Correlation Between News Sentiment and Stock Movement

*   **Objective:** Analyze the correlation between news headline sentiment and daily stock price movements.
*   **Key Activities:**
    *   Loaded processed news data (`data/processed_news_data.pkl`) and stock data with indicators (e.g., `data/TSLA_indicators.pkl`).
    *   Performed sentiment analysis on news headlines using `TextBlob` to get polarity scores.
    *   Aggregated sentiment scores daily for each stock.
    *   Calculated daily stock returns (percentage change in closing price).
    *   Aligned news sentiment dates with stock trading dates and merged the datasets.
    *   Computed Pearson correlation coefficient between average daily sentiment scores and daily stock returns for each stock.
    *   Visualized daily returns vs. sentiment and scatter plots of sentiment vs. returns.
*   **Outputs:**
    *   Visualizations saved in the `Plots-task3/` directory (e.g., `GOOG_sentiment_vs_returns.png`, `correlation_summary.png`).
    *   Correlation results saved to `data/correlation_results.csv`.
*   **notebooks:** `notebooks/News-stock-correlation.ipynb` (or similar)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    The project requires Python 3.8+ and the libraries listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    **Note on TA-Lib:** `TA-Lib` can be tricky to install. Refer to the official [TA-Lib installation guide](https://mrjbq7.github.io/ta-lib/install.html) for your operating system if `pip install TA-Lib` fails. You might need to install the underlying C library first.

4.  **NLTK Data:**
    The project uses NLTK for text processing. Download the necessary resources:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```

5.  **Data:**
    *   Place the `raw_analyst_ratings.csv` file in the `data/` directory.
    *   Place historical stock data CSV files (e.g., `AAPL_historical_data.csv`, `TSLA_historical_data.csv`, etc.) in the `data/` directory. These files should contain 'Date', 'Open', 'High', 'Low', 'Close', 'Volume' columns.

## Usage

The analysis is divided into three main parts, executed by their respective scripts:

1.  **Task 1: EDA & News Preprocessing**
    ```bash
    python notebook/eda.ipynb
    ```
    This script will process `data/raw_analyst_ratings.csv`, perform EDA, save plots to `plots/`, and save the processed news data to `data/processed_news_data.pkl`.

2.  **Task 2: Technical Analysis**
    ```bash
    python notebooks/Quantitative-analysis.ipynb
    ```
    This script loads historical stock CSVs from `data/`, calculates technical indicators, saves plots to `Plots-task2/`, and saves processed stock data with indicators (e.g., `data/AAPL_indicators.pkl`).

3.  **Task 3: Sentiment-Stock Correlation**
    ```bash
    python notebooks/News-stock-correlation.ipynb
    ```
    This script uses the outputs from Task 1 and Task 2 (`processed_news_data.pkl` and `*_indicators.pkl` files) to perform sentiment analysis, calculate correlations, save plots to `Plots-task3/`, and store results in `data/correlation_results.csv`.

Ensure that the scripts are run in order, or that their prerequisite data files are present in the `data/` directory.

## Key Findings (Summary)

*(This section should be updated with specific findings from your analysis after running the scripts)*

*   **EDA (Task 1):**
    *   The distribution of headline lengths showed [e.g., a peak around X characters, a long tail, etc.].
    *   The most active publisher was [e.g., Benzinga Signals], contributing [X]% of articles.
    *   News publication frequency peaked on [e.g., weekdays during market hours], with notable spikes on [specific dates or events, if any].
    *   Common keywords in headlines included [e.g., "target", "rating", "price", "buy", "sell"].

*   **Technical Indicators (Task 2):**
    *   SMA, RSI, and MACD indicators were successfully calculated and visualized for all target stocks (`TSLA`, `NVDA`, `META`, `AMZN`, `GOOG`, `AAPL`, `MSFT`).
    *   These visualizations provide a basis for identifying potential trends, overbought/oversold conditions, and momentum shifts.

*   **Sentiment-Stock Correlation (Task 3):**
    *   Sentiment analysis using TextBlob provided polarity scores for news headlines.
    *   The Pearson correlation between aggregated daily news sentiment and daily stock returns for [e.g., AAPL] was [correlation_value] (p-value: [p_value_value]), indicating a [e.g., weak positive, negligible, etc.] relationship.
    *   *(Summarize overall trends across stocks: e.g., "Most stocks showed a weak but statistically insignificant correlation...", or "NVDA and TSLA exhibited stronger correlations compared to...").*
    *   The `correlation_summary.png` plot provides a visual comparison of correlation coefficients across stocks.

## Future Work & Potential Improvements

*   Utilize more advanced NLP models for sentiment analysis (e.g., FinBERT, VADER).
*   Explore different aggregation methods for daily sentiment (e.g., weighted by publisher reliability or article impact).
*   Investigate lagged correlations (e.g., sentiment today vs. returns tomorrow or intra-day returns).
*   Incorporate time-of-day of news publication more granularly if possible.
*   Develop predictive machine learning models using sentiment scores and technical indicators as features.
*   Expand the dataset to include more stocks or longer time periods.
*   Perform event-based analysis (e.g., impact of earnings announcements vs. general news).
