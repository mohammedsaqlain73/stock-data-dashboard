import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict

class StockDataProcessor:

    NSE_STOCKS = [
        {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries'},
        {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services'},
        {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank'},
        {'symbol': 'INFY.NS', 'name': 'Infosys'},
        {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank'},
        {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever'},
        {'symbol': 'ITC.NS', 'name': 'ITC'},
        {'symbol': 'SBIN.NS', 'name': 'State Bank of India'},
        {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel'},
        {'symbol': 'KOTAKBANK.NS', 'name': 'Kotak Mahindra Bank'},
        {'symbol': 'LT.NS', 'name': 'Larsen & Toubro'},
        {'symbol': 'AXISBANK.NS', 'name': 'Axis Bank'},
        {'symbol': 'WIPRO.NS', 'name': 'Wipro'},
        {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki'},
        {'symbol': 'TITAN.NS', 'name': 'Titan Company'}
    ]

    @staticmethod
    def fetch_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetch stock data from yfinance

        Args:
            symbol: Stock symbol (e.g., 'RELIANCE.NS')
            period: Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y')

        Returns:
            DataFrame with stock data
        """
        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)

            if df.empty:
                return pd.DataFrame()

            df.reset_index(inplace=True)
            df['symbol'] = symbol

            df.columns = df.columns.str.lower()

            return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare stock data

        Args:
            df: Raw stock dataframe

        Returns:
            Cleaned dataframe
        """
        if df.empty:
            return df

        df = df.copy()

        df['date'] = pd.to_datetime(df['date'])

        df = df.dropna(subset=['open', 'high', 'low', 'close'])

        df_temp = df[df['close'] > 0]
        df = df_temp.copy()

        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        result_df: pd.DataFrame = df.dropna(subset=numeric_cols)

        return result_df

    @staticmethod
    def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all required metrics

        Metrics:
        - Daily Return: (CLOSE - OPEN) / OPEN
        - 7-day Moving Average
        - 52-week High/Low
        - Volatility Score (custom metric)

        Args:
            df: Cleaned stock dataframe

        Returns:
            DataFrame with calculated metrics
        """
        if df.empty:
            return df

        df = df.copy()
        df = df.sort_values('date')

        df['daily_return'] = (df['close'] - df['open']) / df['open']

        df['ma_7'] = df['close'].rolling(window=7, min_periods=1).mean()

        df['week_52_high'] = df['high'].rolling(window=252, min_periods=1).max()
        df['week_52_low'] = df['low'].rolling(window=252, min_periods=1).min()

        df['volatility_score'] = df['daily_return'].rolling(window=20, min_periods=1).std() * np.sqrt(252) * 100

        return df

    @staticmethod
    def get_summary_statistics(df: pd.DataFrame) -> Dict:
        """
        Calculate summary statistics for a stock

        Args:
            df: Stock dataframe with calculated metrics

        Returns:
            Dictionary with summary statistics
        """
        if df.empty:
            return {}

        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date']).dt.tz_localize(None)

        cutoff_date = datetime.now() - timedelta(days=365)
        df_year = df_copy[df_copy['date'] >= cutoff_date]

        if df_year.empty:
            df_year = df_copy

        summary = {
            '52_week_high': float(df_year['high'].max()),
            '52_week_low': float(df_year['low'].min()),
            'avg_close': float(df_year['close'].mean()),
            'current_price': float(df.iloc[-1]['close']),
            'total_days': len(df),
            'avg_volume': float(df['volume'].mean()),
            'avg_daily_return': float(df['daily_return'].mean() * 100),
            'volatility': float(df['volatility_score'].iloc[-1]) if 'volatility_score' in df.columns else 0
        }

        return summary

    @staticmethod
    def process_stock(symbol: str, period: str = "1y") -> tuple:
        """
        Complete processing pipeline for a stock

        Args:
            symbol: Stock symbol
            period: Time period

        Returns:
            Tuple of (processed_df, summary_stats)
        """
        df = StockDataProcessor.fetch_stock_data(symbol, period)

        if df.empty:
            return pd.DataFrame(), {}

        df = StockDataProcessor.clean_data(df)
        df = StockDataProcessor.calculate_metrics(df)
        summary = StockDataProcessor.get_summary_statistics(df)

        return df, summary
