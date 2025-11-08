import sqlite3
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime

class StockDatabase:
    def __init__(self, db_name: str = "stock_data.db"):
        self.db_name = db_name
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                symbol TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                last_updated TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                date DATE NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                daily_return REAL,
                ma_7 REAL,
                week_52_high REAL,
                week_52_low REAL,
                volatility_score REAL,
                UNIQUE(symbol, date)
            )
        ''')

        conn.commit()
        conn.close()

    def add_company(self, symbol: str, name: str):
        """Add a new company to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO companies (symbol, name, last_updated)
            VALUES (?, ?, ?)
        ''', (symbol, name, datetime.now()))

        conn.commit()
        conn.close()

    def get_all_companies(self) -> List[Dict]:
        """Get all companies from the database"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM companies", conn)
        conn.close()
        return df.to_dict('records')

    def save_stock_data(self, df: pd.DataFrame):
        """Save stock data to the database"""
        conn = sqlite3.connect(self.db_name)
        df.to_sql('stock_data', conn, if_exists='append', index=False)
        conn.close()

    def get_stock_data(self, symbol: str, days: int = 30) -> pd.DataFrame:
        """Get stock data for a specific symbol"""
        conn = sqlite3.connect(self.db_name)
        query = '''
            SELECT * FROM stock_data
            WHERE symbol = ?
            ORDER BY date DESC
            LIMIT ?
        '''
        df = pd.read_sql_query(query, conn, params=[symbol, days])
        conn.close()
        return df.sort_values('date')

    def get_all_stock_data(self, symbol: str) -> pd.DataFrame:
        """Get all stock data for a specific symbol"""
        conn = sqlite3.connect(self.db_name)
        query = "SELECT * FROM stock_data WHERE symbol = ? ORDER BY date"
        df = pd.read_sql_query(query, conn, params=[symbol])
        conn.close()
        return df

    def get_52_week_summary(self, symbol: str) -> Dict:
        """Get 52-week summary statistics for a symbol"""
        conn = sqlite3.connect(self.db_name)
        query = '''
            SELECT
                MAX(high) as week_52_high,
                MIN(low) as week_52_low,
                AVG(close) as avg_close,
                symbol
            FROM stock_data
            WHERE symbol = ?
            AND date >= date('now', '-365 days')
        '''
        cursor = conn.cursor()
        cursor.execute(query, (symbol,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'symbol': symbol,
                '52_week_high': result[0],
                '52_week_low': result[1],
                'avg_close': result[2]
            }
        return {}

    def clear_stock_data(self, symbol: str):
        """Clear existing stock data for a symbol"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stock_data WHERE symbol = ?", (symbol,))
        conn.commit()
        conn.close()
