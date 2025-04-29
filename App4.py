import pandas as pd
import streamlit as st
from datetime import timedelta

# --- Streamlit Config ---
st.set_page_config(page_title="XAUUSD Fibonacci Demo", layout="wide")
st.markdown("<h3 style='margin-bottom: 0;'>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)

# --- Layout Structure ---
header = st.container()
top_row = st.columns([2, 1])  # 2:1 ratio for chart vs metrics
middle_row = st.columns(2)
chart_container = st.container()

# --- Static Data Generation ---
@st.cache_data
def get_static_data():
    base_price = 1950.00
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq="H")
    return pd.DataFrame({
        "Time": dates,
        "Open": [base_price + i*0.5 for i in range(100)],
        "High": [base_price + i*0.5 + 2.5 for i in range(100)],
        "Low": [base_price + i*0.5 - 2.0 for i in range(100)],
        "Close": [base_price + i*0.5 + 0.3 for i in range(100)],
        "Volume": [100000 + i*500 for i in range(100)]
    }).sort_values("Time")

# --- Mock Data Generation ---
df = get_static_data()
high = df["High"].max()
low = df["Low"].min()

levels = {
    "0.0%": high,
    "23.6%": high - (high - low) * 0.236,
    "38.2%": high - (high - low) * 0.382,
    "50.0%": high - (high - low) * 0.5,
    "61.8%": high - (high - low) * 0.618,
    "78.6%": high - (high - low) * 0.786,
    "100.0%": low,
}

# --- Header Section ---
with header:
    st.markdown("---")
    cols = st.columns(4)
    with cols[0]: st.markdown("<small><b>Current Price:</b> $1975.50</small>", unsafe_allow_html=True)
    with cols[1]: st.markdown("<small><b>Today's High:</b> $2001.00</small>", unsafe_allow_html=True)
    with cols[2]: st.markdown("<small><b>Today's Low:</b> $1948.00</small>", unsafe_allow_html=True)
    with cols[3]: st.markdown("<small><b>24h Change:</b> +1.25%</small>", unsafe_allow_html=True)
    st.markdown("---")

# --- Top Row: Chart + Signal ---
with top_row[0]:  # Chart Column
    st.markdown("<h5>📊 Price Chart</h5>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/1200x400.png?text=Interactive+Chart+Area", 
             use_container_width=True)

with top_row[1]:  # Signal Column
    st.markdown("<h5>🚦 Active Signal</h5>", unsafe_allow_html=True)
    st.markdown("#### 🔴 SELL Recommendation")
    st.markdown("<small><b>Entry Price:</b> 1975.50</small>", unsafe_allow_html=True)
    st.markdown("<small><b>Take Profit:</b> 1962.00</small>", unsafe_allow_html=True)
    st.markdown("<small><b>Stop Loss:</b> 1985.00</small>", unsafe_allow_html=True)
    st.progress(75, text="Signal Strength")

# --- Middle Row: Fibonacci + History ---
with middle_row[0]:
    st.markdown("<h5>📐 Fibonacci Levels</h5>", unsafe_allow_html=True)
    fib_df = pd.DataFrame(levels.items(), columns=["Level", "Price"])
    st.dataframe(
        fib_df.set_index("Level").style.format({"Price": "{:.2f}"}),
        use_container_width=True,
        height=300
    )

with middle_row[1]:
    st.markdown("<h5>🕒 Signal History</h5>", unsafe_allow_html=True)
    history_data = {
        "Time": ["14:30", "13:45", "12:15", "11:00"],
        "Signal": ["🔴 Sell", "🟢 Buy", "⚪ Hold", "🔴 Sell"],
        "Price": ["1975.50", "1968.20", "-", "1972.80"]
    }
    st.dataframe(
        pd.DataFrame(history_data),
        use_container_width=True,
        hide_index=True,
        height=300
    )

# --- Bottom Chart Container ---
with chart_container:
    st.markdown("---")
    st.markdown("<h5>📉 Technical Analysis</h5>", unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]: st.image("https://via.placeholder.com/400x200.png?text=RSI+Indicator")
    with cols[1]: st.image("https://via.placeholder.com/400x200.png?text=MACD+Indicator")
    with cols[2]: st.image("https://via.placeholder.com/400x200.png?text=Volume+Chart")
    st.markdown("---")

# --- Footer ---
st.caption("Demo Data • Updated: 2024-02-21 15:00 UTC")
