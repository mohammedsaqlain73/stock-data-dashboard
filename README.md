# 📊 Stock Data Intelligence Dashboard

A full-stack financial analytics platform for real-time NSE/BSE stock data. Built with Python, FastAPI, and Streamlit, it features automated data collection, REST API endpoints, and interactive visualizations.

<p align="center">
  <img src="https://raw.githubusercontent.com/mohammedsaqlain73/stock-data-dashboard/main/preview1.png" alt="Dashboard Preview 1" width="45%">
  &nbsp;&nbsp;
  <img src="https://raw.githubusercontent.com/mohammedsaqlain73/stock-data-dashboard/main/preview2.png" alt="Dashboard Preview 2" width="45%">
</p>


🔗 **Live Demo:** [https://stock-data-dashboard-jarnox.streamlit.app/](https://stock-data-dashboard-jarnox.streamlit.app/)

---

## 🚀 Features

- **Real-Time Data:** Fetches stock data using `yfinance`
- **Metrics:** Daily return, 7-day moving average, 52-week high/low, custom volatility score
- **REST API (FastAPI):**
  - `/companies`: List available stocks
  - `/data/{symbol}`: Last 30 days of data
  - `/summary/{symbol}`: 52-week summary
- **Dashboard (Streamlit):**
  - Candlestick charts with volume
  - Returns & volatility analysis
  - Summary cards and CSV export
  - Real-time refresh

---

## 🧰 Tech Stack

Python 3.11 · FastAPI · Streamlit · SQLite · yfinance · Pandas · Plotly

---

## 📁 Structure
📦 stock-data-dashboard
│
├── api.py              # FastAPI backend for stock data API
├── app.py              # Streamlit dashboard UI
├── database.py         # SQLite database management
├── data_processor.py   # Fetching, cleaning, and metrics computation
├── main.py             # Entry/test file
├── requirements.txt    # Python dependencies
├── readme.md           # Documentation (this file)
└── .gitignore          # Ignore venv & temp files


---

## 🧰 Technology Stack

| Layer | Technology |
|-------|-------------|
| Language | Python 3.11 |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Database | SQLite |
| Libraries | yfinance, pandas, numpy, plotly |

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repo
```bash
git clone https://github.com/mohammedsaqlain73/stock-data-dashboard.git
cd stock-data-dashboard
2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # (Windows)
--
3️⃣ Install dependencies
pip install -r requirements.txt
--
4️⃣ Start FastAPI backend
python api.py
--
Visit → http://127.0.0.1:8000/docs
 for Swagger UI
--
5️⃣ Start Streamlit dashboard
streamlit run app.py
Visit → http://localhost:8501
--
🧠 Example API Endpoints
Root:
GET http://localhost:8000/
--
Companies:
GET http://localhost:8000/companies
--
Stock Data:
GET http://localhost:8000/data/RELIANCE.NS
--
Summary:
GET http://localhost:8000/summary/TCS.NS
