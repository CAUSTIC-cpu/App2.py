import pandas as pd
import streamlit as st
import requests
import json
import streamlit.components.v1 as components

# --- Streamlit Config ---
st.set_page_config(page_title="XAUUSD Fibonacci Demo", layout="wide")
st.markdown("<h3 style='margin-bottom: 0;'>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)

# --- Layout Structure ---
header = st.container()
top_row = st.columns([2, 1])
middle_row = st.columns(2)
chart_container = st.container()

# --- API Settings ---
API_KEY = "your_twelve_data_api_key"  # Replace with your Twelve Data API Key
BASE_URL = "https://api.twelvedata.com/"

# --- Fetch Data from Twelve Data API ---
def get_xauusd_data():
    url = f"{BASE_URL}time_series"
    params = {
        "symbol": "XAU/USD",
        "interval": "1h",
        "apikey": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching XAU/USD data: {e}")
        return None

def get_technical_summary():
    url = f"{BASE_URL}technical_indicators"
    params = {
        "symbol": "XAU/USD",
        "interval": "1h",
        "indicators": "rsi,macd",
        "apikey": API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching technical summary: {e}")
        return None

# --- Fetch Data ---
xau_data = get_xauusd_data()
technical_summary = get_technical_summary()

# Check if data was fetched successfully
if xau_data and technical_summary:
    # --- Process Data ---
    def process_data(xau_data):
        df = pd.DataFrame(xau_data['values'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        df = df[['open', 'high', 'low', 'close', 'volume']]
        df = df.astype(float)
        return df

    xau_df = process_data(xau_data)

    # --- Header Section ---
    with header:
        st.markdown("---")
        cols = st.columns(4)
        with cols[0]: st.markdown(f"<small><b>Current Price:</b> {xau_df['close'].iloc[-1]:.2f}</small>", unsafe_allow_html=True)
        with cols[1]: st.markdown(f"<small><b>Today's High:</b> {xau_df['high'].max():.2f}</small>", unsafe_allow_html=True)
        with cols[2]: st.markdown(f"<small><b>Today's Low:</b> {xau_df['low'].min():.2f}</small>", unsafe_allow_html=True)
        with cols[3]: st.markdown(f"<small><b>24h Change:</b> {((xau_df['close'].iloc[-1] - xau_df['close'].iloc[0]) / xau_df['close'].iloc[0])*100:.2f}%</small>", unsafe_allow_html=True)
        st.markdown("---")

    # --- Top Row: Live Chart & Signal Box ---
    with top_row[0]:  # Chart
        st.markdown("<h5>📊 Live Chart (Twelve Data)</h5>", unsafe_allow_html=True)
        
        # Embed TradingView chart as placeholder (use Twelve Data charting if desired)
        tv_chart = """
        <div class="tradingview-widget-container" style="height:420px;">
          <iframe src="https://s.tradingview.com/embed-widget/advanced-chart/?symbol=OANDA:XAUUSD&theme=dark&style=1&locale=en&toolbar_bg=1e1e1e&studies=[]&hide_side_toolbar=false&withdateranges=true&hideideas=true&interval=60&allow_symbol_change=true"
            style="width:100%;height:420px;" frameborder="0" allowtransparency="true" scrolling="no">
          </iframe>
        </div>
        """
        components.html(tv_chart, height=420)

    with top_row[1]:  # Active Signal
        st.markdown("<h5>🚦 Active Signal</h5>", unsafe_allow_html=True)
        st.markdown(f"#### 🔴 SELL Recommendation")
        st.markdown(f"<small><b>Entry Price:</b> {xau_df['close'].iloc[-1]:.2f}</small>", unsafe_allow_html=True)
        st.markdown(f"<small><b>Take Profit:</b> {xau_df['close'].iloc[-1] - 10:.2f}</small>", unsafe_allow_html=True)
        st.markdown(f"<small><b>Stop Loss:</b> {xau_df['close'].iloc[-1] + 10:.2f}</small>", unsafe_allow_html=True)
        st.progress(75, text="Signal Strength")

    # --- Middle Row: Technical Summary (Real-Time from Twelve Data) ---
    with middle_row[0]:
        st.markdown("<h5>🧠 Technical Summary</h5>", unsafe_allow_html=True)
        if "technical_indicators" in technical_summary:
            indicators = technical_summary["technical_indicators"]
            summary_df = pd.DataFrame(indicators)
            st.dataframe(summary_df[['indicator', 'value']], use_container_width=True, height=300)
        else:
            st.write("No technical data available at the moment.")

    with middle_row[1]:
        st.markdown("<h5>🕒 Signal History</h5>", unsafe_allow_html=True)
        signal_history = {
            "Time": ["14:30", "13:45", "12:15", "11:00"],
            "Signal": ["🔴 Sell", "🟢 Buy", "⚪ Hold", "🔴 Sell"],
            "Price": ["1975.50", "1968.20", "-", "1972.80"]
        }
        st.dataframe(pd.DataFrame(signal_history), use_container_width=True, hide_index=True, height=300)

    # --- Bottom Technical Placeholder ---
    with chart_container:
        st.markdown("---")
        st.markdown("<h5>📉 Technical Indicators</h5>", unsafe_allow_html=True)
        cols = st.columns(3)
        with cols[0]: st.image("https://via.placeholder.com/400x200.png?text=RSI+Indicator")
        with cols[1]: st.image("https://via.placeholder.com/400x200.png?text=MACD+Indicator")
        with cols[2]: st.image("https://via.placeholder.com/400x200.png?text=Volume+Chart")
        st.markdown("---")

    # --- Footer ---
    st.caption("Demo Data • Updated: 2024-02-21 15:00 UTC")
else:
    st.error("Failed to fetch data. Please check your API key or try again later.")
