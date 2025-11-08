# stock-data-dashboard 
Stock Data Intelligence Dashboard
Internship Assignment - Financial Data Platform
A comprehensive financial data platform demonstrating real-world stock market data collection, processing, REST API development, and interactive data visualization for NSE/BSE stocks.

Features
Data Collection & Processing
Automated Stock Data Fetching: Uses yfinance API to fetch real-time NSE/BSE stock market data
Data Cleaning Pipeline: Handles missing values, incorrect formats, and data validation using Pandas
Calculated Metrics:
Daily Return: (CLOSE - OPEN) / OPEN
7-Day Moving Average
52-Week High/Low
Custom Volatility Score: Annualized standard deviation of returns (20-day rolling window)
REST API Backend (FastAPI)
Three fully functional REST endpoints as per assignment requirements:

GET /companies - Returns list of all available companies
GET /data/{symbol} - Returns last 30 days of stock data
GET /summary/{symbol} - Returns 52-week high, low, and average close
Interactive Dashboard (Streamlit)
Professional candlestick charts with volume overlay
Moving average trend visualization
Daily returns and volatility analysis
Summary statistics cards
Data table with CSV export
Real-time data refresh capability
Technology Stack
Language: Python 3.11
Backend Framework: FastAPI
Frontend Framework: Streamlit
Database: SQLite
Libraries:
yfinance (Stock data)
Pandas & NumPy (Data processing)
Plotly (Interactive charts)
Uvicorn (ASGI server)
Project Structure
.
├── api.py                  # FastAPI REST API endpoints
├── app.py                  # Streamlit dashboard application
├── database.py             # SQLite database management
├── data_processor.py       # Stock data collection & processing
├── stock_data.db          # SQLite database (auto-generated)
└── README.md              # This file

Installation & Setup
Clone/Access the project

Install dependencies (already configured in Replit):

pip install yfinance fastapi uvicorn pandas numpy plotly streamlit

Run the applications:
Option 1: Using Replit (Recommended)

The workflows are pre-configured
Streamlit dashboard runs on port 5000
FastAPI server runs on port 8000
Option 2: Manual execution

# Terminal 1 - Start Streamlit Dashboard
streamlit run app.py --server.port 5000
# Terminal 2 - Start FastAPI Server
python api.py

API Documentation
Base URL
http://localhost:8000

Endpoints
1. GET /companies
Returns a list of all available companies.

Request:

curl http://localhost:8000/companies

Response:

[
  {
    "symbol": "RELIANCE.NS",
    "name": "Reliance Industries",
    "last_updated": "2025-11-08 14:46:27.754462"
  },
  {
    "symbol": "TCS.NS",
    "name": "Tata Consultancy Services",
    "last_updated": "2025-11-08 14:46:27.836803"
  }
]

2. GET /data/{symbol}
Returns the last 30 days of stock data for a given symbol (configurable via query parameter).

Parameters:

symbol (path): Stock symbol (e.g., RELIANCE.NS)
days (query, optional): Number of days to retrieve (default: 30)
Request:

curl "http://localhost:8000/data/RELIANCE.NS?days=5"

Response:

{
  "symbol": "RELIANCE.NS",
  "days_returned": 5,
  "data": [
    {
      "date": "2025-11-07",
      "open": 1494.60,
      "high": 1498.40,
      "low": 1475.90,
      "close": 1478.00,
      "volume": 7821765,
      "daily_return": -0.0111,
      "ma_7": 1482.84,
      "week_52_high": 1544.83,
      "week_52_low": 1110.42,
      "volatility_score": 15.14
    }
  ]
}

3. GET /summary/{symbol}
Returns 52-week summary statistics for a symbol.

Parameters:

symbol (path): Stock symbol (e.g., TCS.NS)
Request:

curl http://localhost:8000/summary/TCS.NS

Response:

{
  "symbol": "TCS.NS",
  "52_week_high": 4343.80,
  "52_week_low": 2855.95,
  "avg_close": 3483.78,
  "current_price": 2991.80,
  "avg_daily_return_percent": -0.106,
  "volatility_score": 11.65,
  "avg_volume": 2600210.35,
  "total_days": 249
}

Available Stock Symbols
RELIANCE.NS - Reliance Industries
TCS.NS - Tata Consultancy Services
HDFCBANK.NS - HDFC Bank
INFY.NS - Infosys
ICICIBANK.NS - ICICI Bank
HINDUNILVR.NS - Hindustan Unilever
ITC.NS - ITC
SBIN.NS - State Bank of India
BHARTIARTL.NS - Bharti Airtel
KOTAKBANK.NS - Kotak Mahindra Bank
LT.NS - Larsen & Toubro
AXISBANK.NS - Axis Bank
WIPRO.NS - Wipro
MARUTI.NS - Maruti Suzuki
TITAN.NS - Titan Company
Dashboard Features
1. Price Chart Tab
Interactive candlestick chart showing OHLC (Open, High, Low, Close) data
7-day moving average overlay
Volume bars
Zoom and pan capabilities
2. Returns & Volatility Tab
Daily returns bar chart (color-coded: green for gains, red for losses)
Volatility score trend line
Historical volatility analysis
3. Data Table Tab
Last 30 days of detailed stock data
Sortable columns
CSV export functionality
Formatted values with currency symbols
4. Summary Tab
Key price metrics (52-week high/low, average close, current price)
Performance metrics (average daily return, volatility score, volume)
Volatility score explanation and interpretation guide
Custom Metric: Volatility Score
The Volatility Score is a custom analytical metric that measures stock price stability:

Formula:

Volatility Score = σ(daily_returns, 20-day) × √252 × 100

Interpretation:

Low Volatility (< 20%): Stable stock with predictable movements
Medium Volatility (20-40%): Moderate price fluctuations
High Volatility (> 40%): Significant price swings, higher risk/reward
This metric helps investors:

Assess investment risk
Compare stability across different stocks
Make informed portfolio decisions
Identify trading opportunities
Data Pipeline
Data Collection: yfinance API fetches historical stock data
Data Cleaning:
Remove missing values
Validate numeric formats
Convert date columns
Filter invalid entries
Metric Calculation:
Compute daily returns
Calculate moving averages
Determine 52-week highs/lows
Generate volatility scores
Storage: Save processed data to SQLite database
API/Dashboard: Serve data via REST endpoints and interactive UI
Technical Highlights
Backend (FastAPI)
RESTful API design with proper HTTP methods
Automatic interactive API documentation (Swagger UI at /docs)
CORS enabled for frontend integration
Comprehensive error handling
Type hints and Pydantic models
Frontend (Streamlit)
Responsive wide layout
Real-time data refresh
Professional Plotly visualizations
Caching for improved performance
User-friendly interface with tabs and cards
Database (SQLite)
Efficient data storage and retrieval
Indexed queries for fast lookups
Automatic timestamp tracking
Relational schema design
Testing the Application
Test the Dashboard
Open the Streamlit app (port 5000)
Select a company from the dropdown
Explore different tabs (Price Chart, Returns & Volatility, Data Table, Summary)
Click "Refresh Data" to fetch latest stock information
Download CSV data from the Data Table tab
Test the API
# Test root endpoint
curl http://localhost:8000/
# Get all companies
curl http://localhost:8000/companies
# Get 30 days of stock data
curl http://localhost:8000/data/RELIANCE.NS
# Get 7 days of stock data
curl "http://localhost:8000/data/TCS.NS?days=7"
# Get summary statistics
curl http://localhost:8000/summary/INFY.NS

Interactive API Documentation
Visit http://localhost:8000/docs for Swagger UI with:

Interactive endpoint testing
Request/response schemas
Example values
Try-it-out functionality
Future Enhancements
Correlation analysis between multiple stocks
Batch data download for all NSE/BSE stocks via bhavcopy CSVs
Advanced technical indicators (RSI, MACD, Bollinger Bands)
PostgreSQL database for production deployment
Comparative analysis for side-by-side stock comparison
Real-time price alerts and notifications
Historical backtesting capabilities
Portfolio tracking and analysis
Assignment Completion Checklist
✅ Part 1 - Data Collection & Preparation

 Collect stock market data using yfinance API
 Clean and organize data with Pandas
 Handle missing values and incorrect formats
 Convert date columns properly
 Add calculated metrics:
 Daily Return
 7-day Moving Average
 52-week High/Low
 Custom metric: Volatility Score
✅ Part 2 - Backend API Development

 GET /companies - List all companies
 GET /data/{symbol} - Last 30 days stock data
 GET /summary/{symbol} - 52-week statistics
✅ Bonus Features

 Interactive Streamlit dashboard
 Professional data visualizations
 SQLite database integration
 Comprehensive documentation
 Production-ready code structure
