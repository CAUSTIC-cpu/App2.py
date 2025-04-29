import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# --- Streamlit Config ---
st.set_page_config(page_title="XAUUSD Fibonacci Demo", layout="wide")
st.markdown("<h3 style='margin-bottom: 0;'>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)

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

# --- Header Section ---
with header:
    st.markdown("---")
    cols = st.columns(4)
    with cols[0]: st.markdown("<small><b>Current Price:</b> $1975.50</small>", unsafe_allow_html=True)
    with cols[1]: st.markdown("<small><b>Today's High:</b> $2001.00</small>", unsafe_allow_html=True)
    with cols[2]: st.markdown("<small><b>Today's Low:</b> $1948.00</small>", unsafe_allow_html=True)
    with cols[3]: st.markdown("<small><b>24h Change:</b> +1.25%</small>", unsafe_allow_html=True)
    st.markdown("---")

# --- Top Row: TradingView Chart & Signal Box ---
with top_row[0]:  # Chart
    st.markdown("<h5>📊 Live Chart (TradingView)</h5>", unsafe_allow_html=True)
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
    st.markdown("#### 🔴 SELL Recommendation")
    st.markdown("<small><b>Entry Price:</b> 1975.50</small>", unsafe_allow_html=True)
    st.markdown("<small><b>Take Profit:</b> 1962.00</small>", unsafe_allow_html=True)
    st.markdown("<small><b>Stop Loss:</b> 1985.00</small>", unsafe_allow_html=True)
    st.progress(75, text="Signal Strength")

# --- Middle Row: Technical Summary (Mocked) + Placeholder for Levels/History ---
with middle_row[0]:
    st.markdown("<h5>🧠 Technical Summary</h5>", unsafe_allow_html=True)
    tech_summary = get_static_technical_summary()
    summary_df = pd.DataFrame(tech_summary)
    st.dataframe(summary_df, use_container_width=True, height=300)

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
