from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uvicorn
from database import StockDatabase
from data_processor import StockDataProcessor
import pandas as pd

app = FastAPI(
    title="Stock Data Intelligence API",
    description="REST API for NSE/BSE stock market data with calculated metrics",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = StockDatabase()

for stock in StockDataProcessor.NSE_STOCKS:
    db.add_company(stock['symbol'], stock['name'])

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Stock Data Intelligence API",
        "version": "1.0.0",
        "endpoints": {
            "/companies": "Get list of all available companies",
            "/data/{symbol}": "Get last 30 days of stock data for a symbol",
            "/summary/{symbol}": "Get 52-week summary statistics for a symbol"
        },
        "example_symbols": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS"]
    }

@app.get("/companies", response_model=List[Dict])
def get_companies():
    """
    Returns a list of all available companies

    Returns:
        List of dictionaries containing symbol, name, and last_updated timestamp
    """
    try:
        companies = db.get_all_companies()
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching companies: {str(e)}")

@app.get("/data/{symbol}")
def get_stock_data(symbol: str, days: int = 30):
    """
    Returns last N days of stock data for a given symbol

    Args:
        symbol: Stock symbol (e.g., 'RELIANCE.NS')
        days: Number of days to retrieve (default: 30)

    Returns:
        Dictionary containing symbol and list of daily stock data with metrics
    """
    try:
        df = db.get_all_stock_data(symbol)

        if df.empty:
            df, summary = StockDataProcessor.process_stock(symbol, period="1y")
            if not df.empty:
                df_to_save = df[['symbol', 'date', 'open', 'high', 'low', 'close',
                                'volume', 'daily_return', 'ma_7', 'week_52_high',
                                'week_52_low', 'volatility_score']].copy()
                db.save_stock_data(df_to_save)

        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")

        df = df.tail(days)

        df['date'] = pd.to_datetime(df['date']).astype(str)

        data_records = df.to_dict('records')

        return {
            "symbol": symbol,
            "days_returned": len(data_records),
            "data": data_records
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")

@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    """
    Returns 52-week summary statistics for a symbol

    Args:
        symbol: Stock symbol (e.g., 'RELIANCE.NS')

    Returns:
        Dictionary with 52-week high, low, average close, and additional metrics
    """
    try:
        df = db.get_all_stock_data(symbol)

        if df.empty:
            df, summary = StockDataProcessor.process_stock(symbol, period="1y")
            if not df.empty:
                df_to_save = df[['symbol', 'date', 'open', 'high', 'low', 'close',
                                'volume', 'daily_return', 'ma_7', 'week_52_high',
                                'week_52_low', 'volatility_score']].copy()
                db.save_stock_data(df_to_save)

        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")

        summary = StockDataProcessor.get_summary_statistics(df)

        return {
            "symbol": symbol,
            "52_week_high": summary.get('52_week_high', 0),
            "52_week_low": summary.get('52_week_low', 0),
            "avg_close": summary.get('avg_close', 0),
            "current_price": summary.get('current_price', 0),
            "avg_daily_return_percent": summary.get('avg_daily_return', 0),
            "volatility_score": summary.get('volatility', 0),
            "avg_volume": summary.get('avg_volume', 0),
            "total_days": summary.get('total_days', 0)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching summary: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
