import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from database import StockDatabase
from data_processor import StockDataProcessor
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Stock Data Intelligence Dashboard By Jarnox",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_database():
    """Initialize and return database instanCE"""
    return StockDatabase()

def load_stock_data(symbol: str, refresh: bool = False):
    """Load stock data from database or fetch new data"""
    db = get_database()

    if refresh:
        with st.spinner(f'Fetching latest data for {symbol}...'):
            df, summary = StockDataProcessor.process_stock(symbol, period="1y")
            if not df.empty:
                db.clear_stock_data(symbol)
                df_to_save = df[['symbol', 'date', 'open', 'high', 'low', 'close',
                                'volume', 'daily_return', 'ma_7', 'week_52_high',
                                'week_52_low', 'volatility_score']].copy()
                db.save_stock_data(df_to_save)
                return df, summary

    df = db.get_all_stock_data(symbol)

    if df.empty:
        with st.spinner(f'Loading data for {symbol}...'):
            df, summary = StockDataProcessor.process_stock(symbol, period="1y")
            if not df.empty:
                df_to_save = df[['symbol', 'date', 'open', 'high', 'low', 'close',
                                'volume', 'daily_return', 'ma_7', 'week_52_high',
                                'week_52_low', 'volatility_score']].copy()
                db.save_stock_data(df_to_save)
    else:
        df['date'] = pd.to_datetime(df['date'])
        summary = StockDataProcessor.get_summary_statistics(df)

    return df, summary

def create_candlestick_chart(df: pd.DataFrame, symbol: str):
    """Create an interactive candlestick chart with moving average"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=(f'{symbol} - Stock Price & 7-Day MA', 'Volume')
    )

    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['ma_7'],
            mode='lines',
            name='7-Day MA',
            line=dict(color='orange', width=2)
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(
            x=df['date'],
            y=df['volume'],
            name='Volume',
            marker_color='lightblue'
        ),
        row=2, col=1
    )

    fig.update_layout(
        height=600,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )

    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig

def create_volatility_chart(df: pd.DataFrame):
    """Create volatility trend chart"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['volatility_score'],
            mode='lines',
            name='Volatility Score',
            fill='tozeroy',
            line=dict(color='red', width=2)
        )
    )

    fig.update_layout(
        title='Volatility Score (20-day rolling)',
        xaxis_title='Date',
        yaxis_title='Volatility (%)',
        height=300,
        hovermode='x unified'
    )

    return fig

def create_returns_chart(df: pd.DataFrame):
    """Create daily returns chart"""
    df_copy = df.copy()
    df_copy['color'] = df_copy['daily_return'].apply(lambda x: 'green' if x >= 0 else 'red')

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_copy['date'],
            y=df_copy['daily_return'] * 100,
            marker_color=df_copy['color'],
            name='Daily Return'
        )
    )

    fig.update_layout(
        title='Daily Returns (%)',
        xaxis_title='Date',
        yaxis_title='Return (%)',
        height=300,
        hovermode='x unified'
    )

    return fig

def main():
    st.title("📈 Stock Data Intelligence Dashboard By Jarnox")
    st.markdown("### Internship Assignment - Financial Data Platform")

    db = get_database()

    for stock in StockDataProcessor.NSE_STOCKS:
        db.add_company(stock['symbol'], stock['name'])

    companies = db.get_all_companies()

    st.sidebar.header("⚙️ Configuration")

    company_names = {f"{c['name']} ({c['symbol']})": c['symbol'] for c in companies}
    selected_company = st.sidebar.selectbox(
        "Select Company",
        options=list(company_names.keys())
    )
    symbol = company_names[selected_company]

    refresh_data = st.sidebar.button("🔄 Refresh Data", use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Features")
    st.sidebar.markdown("""
    - Real-time NSE stock data
    - Daily return calculations
    - 7-day moving average
    - 52-week high/low tracking
    - Custom volatility scoring
    - Interactive visualizations
    """)

    df, summary = load_stock_data(symbol, refresh=refresh_data)

    if df.empty:
        st.error(f"No data available for {symbol}")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Current Price",
            value=f"₹{summary.get('current_price', 0):.2f}",
            delta=f"{summary.get('avg_daily_return', 0):.2f}%"
        )

    with col2:
        st.metric(
            label="52-Week High",
            value=f"₹{summary.get('52_week_high', 0):.2f}"
        )

    with col3:
        st.metric(
            label="52-Week Low",
            value=f"₹{summary.get('52_week_low', 0):.2f}"
        )

    with col4:
        st.metric(
            label="Volatility Score",
            value=f"{summary.get('volatility', 0):.2f}%"
        )

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Price Chart", "📈 Returns & Volatility", "📋 Data Table", "📑 Summary"])

    with tab1:
        st.plotly_chart(create_candlestick_chart(df, symbol), use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_returns_chart(df), use_container_width=True)
        with col2:
            st.plotly_chart(create_volatility_chart(df), use_container_width=True)

    with tab3:
        st.subheader("Last 30 Days Data")
        display_df = df.tail(30)[['date', 'open', 'high', 'low', 'close', 'volume',
                                   'daily_return', 'ma_7', 'volatility_score']].copy()
        display_df['daily_return'] = display_df['daily_return'] * 100
        display_df['date'] = display_df['date'].astype(str).str[:10]

        display_df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume',
                              'Daily Return (%)', '7-Day MA', 'Volatility Score']

        st.dataframe(
            display_df.style.format({
                'Open': '₹{:.2f}',
                'High': '₹{:.2f}',
                'Low': '₹{:.2f}',
                'Close': '₹{:.2f}',
                'Volume': '{:,.0f}',
                'Daily Return (%)': '{:.2f}%',
                '7-Day MA': '₹{:.2f}',
                'Volatility Score': '{:.2f}%'
            }),
            use_container_width=True,
            height=400
        )

        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"{symbol}_data.csv",
            mime="text/csv"
        )

    with tab4:
        st.subheader("Summary Statistics")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Price Metrics")
            st.write(f"**52-Week High:** ₹{summary.get('52_week_high', 0):.2f}")
            st.write(f"**52-Week Low:** ₹{summary.get('52_week_low', 0):.2f}")
            st.write(f"**Average Close:** ₹{summary.get('avg_close', 0):.2f}")
            st.write(f"**Current Price:** ₹{summary.get('current_price', 0):.2f}")

        with col2:
            st.markdown("#### 📈 Performance Metrics")
            st.write(f"**Average Daily Return:** {summary.get('avg_daily_return', 0):.2f}%")
            st.write(f"**Volatility Score:** {summary.get('volatility', 0):.2f}%")
            st.write(f"**Average Volume:** {summary.get('avg_volume', 0):,.0f}")
            st.write(f"**Total Days:** {summary.get('total_days', 0)}")

        st.markdown("---")
        st.markdown("#### 💡 Custom Metric: Volatility Score")
        st.info("""
        The **Volatility Score** is a custom metric that measures the annualized standard deviation
        of daily returns over a 20-day rolling window. A higher score indicates greater price volatility
        and potential risk. This metric helps investors understand the stock's price stability.

        - **Low Volatility (< 20%)**: Stable stock with predictable price movements
        - **Medium Volatility (20-40%)**: Moderate price fluctuations
        - **High Volatility (> 40%)**: Significant price swings, higher risk/reward
        """)

if __name__ == "__main__":
    main()
