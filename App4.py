import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import random

# --- Streamlit Config ---
st.set_page_config(page_title="XAUUSD Fibonacci Demo", layout="wide")
st.markdown("<h3 style='margin-bottom: 0;'>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)

# --- Simulate Live Price ---
if "live_price" not in st.session_state:
    st.session_state.live_price = 1975.50

def update_live_price():
    st.session_state.live_price += random.uniform(-0.5, 0.5)
    st.session_state.live_price = round(st.session_state.live_price, 2)

update_live_price()

# --- Layout Structure ---
header = st.container()
top_row = st.columns([2, 1])
middle_row = st.columns(2)
chart_container = st.container()

# --- Static Mock Data ---
@st.cache_data
def get_static_technical_summary():
    return {
        "Timeframe": ["1 min", "5 min", "15 min", "1 hour", "4 hour", "1 day"],
        "Summary": ["Sell", "Sell", "Neutral", "Buy", "Strong Buy", "Strong Buy"],
        "RSI": [45.2, 48.0, 50.1, 55.2, 61.5, 64.0],
        "MACD": ["Bearish", "Bearish", "Neutral", "Bullish", "Bullish", "Bullish"]
    }

signals = [
    {"time": "14:30", "type": "SELL", "entry": 1975.50, "tp": 1962.00, "sl": 1985.00, "volume": 18250, "max_volume": 25000, "strength": 75},
    {"time": "13:45", "type": "BUY",  "entry": 1968.20, "tp": 1980.00, "sl": 1960.00, "volume": 20000, "max_volume": 25000, "strength": 68},
    {"time": "13:00", "type": "HOLD", "entry": None,     "tp": None,    "sl": None,    "volume": 15000, "max_volume": 25000, "strength": 50},
    {"time": "12:15", "type": "SELL", "entry": 1972.80, "tp": 1960.00, "sl": 1983.00, "volume": 21000, "max_volume": 25000, "strength": 80},
    {"time": "11:30", "type": "BUY",  "entry": 1965.00, "tp": 1975.00, "sl": 1958.00, "volume": 22000, "max_volume": 25000, "strength": 77},
    {"time": "10:45", "type": "SELL", "entry": 1980.00, "tp": 1967.00, "sl": 1988.00, "volume": 19500, "max_volume": 25000, "strength": 72},
    {"time": "10:00", "type": "BUY",  "entry": 1962.00, "tp": 1972.00, "sl": 1955.00, "volume": 24000, "max_volume": 25000, "strength": 82},
    {"time": "09:30", "type": "SELL", "entry": 1970.00, "tp": 1958.00, "sl": 1978.00, "volume": 18000, "max_volume": 25000, "strength": 70},
    {"time": "08:45", "type": "HOLD", "entry": None,     "tp": None,    "sl": None,    "volume": 16000, "max_volume": 25000, "strength": 55},
    {"time": "08:00", "type": "BUY",  "entry": 1955.00, "tp": 1968.00, "sl": 1948.00, "volume": 23000, "max_volume": 25000, "strength": 79},
]

# --- Header Section ---
with header:
    st.markdown("---")
    cols = st.columns(4)
    with cols[0]: st.markdown(f"<small><b>Current Price:</b> ${st.session_state.live_price:.2f}</small>", unsafe_allow_html=True)
    with cols[1]: st.markdown("<small><b>Today's High:</b> $2001.00</small>", unsafe_allow_html=True)
    with cols[2]: st.markdown("<small><b>Today's Low:</b> $1948.00</small>", unsafe_allow_html=True)
    with cols[3]: st.markdown("<small><b>24h Change:</b> +1.25%</small>", unsafe_allow_html=True)
    st.markdown("---")

# --- Top Row: Chart & Active Signal ---
with top_row[0]:
    st.markdown("<h5>📊 Live Chart (TradingView)</h5>", unsafe_allow_html=True)
    tv_chart = """
    <div class="tradingview-widget-container" style="height:420px;">
      <iframe src="https://s.tradingview.com/embed-widget/advanced-chart/?symbol=OANDA:XAUUSD&theme=dark&style=1&locale=en&toolbar_bg=1e1e1e&studies=[]&hide_side_toolbar=false&withdateranges=true&hideideas=true&interval=60&allow_symbol_change=true"
        style="width:100%;height:420px;" frameborder="0" allowtransparency="true" scrolling="no">
      </iframe>
    </div>
    """
    components.html(tv_chart, height=420)

with top_row[1]:
    st.markdown("<h5>🚦 Active Signal</h5>", unsafe_allow_html=True)
    signal = signals[0]
    volume_pct = (signal["volume"] / signal["max_volume"]) * 100
    icon = "🔴" if signal["type"] == "SELL" else "🟢" if signal["type"] == "BUY" else "⚪"
    st.markdown(f"#### {icon} {signal['type']} Recommendation")
    st.markdown(f"<small><b>Entry Price:</b> {signal['entry']}</small>", unsafe_allow_html=True)
    st.markdown(f"<small><b>Take Profit:</b> {signal['tp']}</small>", unsafe_allow_html=True)
    st.markdown(f"<small><b>Stop Loss:</b> {signal['sl']}</small>", unsafe_allow_html=True)
    st.markdown(f"<small><b>Volume:</b> {signal['volume']:,} ({volume_pct:.1f}%)</small>", unsafe_allow_html=True)
    st.progress(signal["strength"], text="Signal Strength")

    # --- Complementary Indicator Confidence ---
    stochastic_pct = min(100, max(0, signal["strength"] + random.randint(-15, 15)))
    atr_pct = min(100, max(0, 100 - abs(signal["strength"] - 70) + random.randint(-10, 10)))

    st.markdown("**Complementary Indicator Confidence:**")
    st.markdown(f"<small><b>Stochastic Oscillator Match:</b> {stochastic_pct:.1f}%</small>", unsafe_allow_html=True)
    st.progress(stochastic_pct, text="Stochastic Confidence")

    st.markdown(f"<small><b>ATR Volatility Context:</b> {atr_pct:.1f}%</small>", unsafe_allow_html=True)
    st.progress(atr_pct, text="ATR Confidence")

# --- Middle Row: Technical Summary + History ---
with middle_row[0]:
    st.markdown("<h5>🧠 Technical Summary</h5>", unsafe_allow_html=True)
    summary_df = pd.DataFrame(get_static_technical_summary())
    st.dataframe(summary_df, use_container_width=True, height=300)

with middle_row[1]:
    st.markdown("<h5>🕒 Signal History</h5>", unsafe_allow_html=True)
    history = {
        "Time": [s["time"] for s in signals[1:]],
        "Signal": ["🔴 Sell" if s["type"] == "SELL" else "🟢 Buy" if s["type"] == "BUY" else "⚪ Hold" for s in signals[1:]],
        "Price": [f"{s['entry']:.2f}" if s["entry"] else "-" for s in signals[1:]]
    }
    st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True, height=300)

# --- Chart Indicators Placeholder ---
with chart_container:
    st.markdown("---")
    st.markdown("<h5>📉 Technical Indicators</h5>", unsafe_allow_html=True)
    cols = st.columns(3)
    import matplotlib.pyplot as plt
import numpy as np


# --- Footer ---
st.caption("Demo Data • Last Updated: " + time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))

# --- Refresh Logic (every 60s) ---
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 60:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()
