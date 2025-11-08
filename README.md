# 📊 Stock Data Intelligence Dashboard

A full-stack financial analytics platform for real-time NSE/BSE stock data. Built with Python, FastAPI, and Streamlit, it features automated data collection, REST API endpoints, and interactive visualizations.

| Preview 1 | Preview 2 |
|------------|------------|
| ![Preview 1](https://raw.githubusercontent.com/mohammedsaqlain73/stock-data-dashboard/main/preview1.png) | ![Preview 2](https://raw.githubusercontent.com/mohammedsaqlain73/stock-data-dashboard/main/preview2.png) |



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


---

### 🧩 File Details

| File | Description |
|------|--------------|
| **`api.py`** | Contains all FastAPI routes — serves stock data and analytics as JSON. |
| **`app.py`** | Streamlit web app for visualizing market data interactively. |
| **`data_processor.py`** | Fetches NSE/BSE stock data using `yfinance`, calculates moving averages, volatility, etc. |
| **`database.py`** | Manages SQLite storage for company info and historical stock data. |
| **`main.py`** | Simple entry/test script to validate setup. |
| **`requirements.txt`** | Lists dependencies required for local and cloud deployment. |
| **`preview1.png`, `preview2.png`** | Images used in README for live demo preview. |
| **`venv/`** | Local virtual environment (not included in GitHub repo). |

---




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
