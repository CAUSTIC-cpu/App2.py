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

# --- Generate Dynamic Signal (Simulate Update) ---
def generate_signal():
    types = ["BUY", "SELL", "HOLD"]
    t = random.choice(types)
    base = round(st.session_state.live_price + random.uniform(-5, 5), 2)
    return {
        "time": time.strftime("%H:%M"),
        "type": t,
        "entry": base if t != "HOLD" else None,
        "tp": round(base + random.uniform(5, 12), 2) if t == "BUY" else round(base - random.uniform(5, 12), 2) if t == "SELL" else None,
        "sl": round(base - random.uniform(4, 8), 2) if t == "BUY" else round(base + random.uniform(4, 8), 2) if t == "SELL" else None,
        "volume": random.randint(15000, 25000),
        "max_volume": 25000,
        "strength": random.randint(60, 90),
    }

# Store signals
if "active_signal" not in st.session_state:
    st.session_state.active_signal = generate_signal()

# --- Layout Structure ---
header = st.container()
top_row = st.columns([2, 1])
middle_row = st.columns(2)

# --- Static Summary ---
@st.cache_data
def get_static_technical_summary():
    return {
        "Timeframe": ["1 min", "5 min", "15 min", "1 hour", "4 hour", "1 day"],
        "Summary": ["Sell", "Sell", "Neutral", "Buy", "Strong Buy", "Strong Buy"],
        "RSI": [45.2, 48.0, 50.1, 55.2, 61.5, 64.0],
        "MACD": ["Bearish", "Bearish", "Neutral", "Bullish", "Bullish", "Bullish"]
    }

# Mock historical signals
signals = [generate_signal() for _ in range(10)]

# --- Header ---
with header:
    st.markdown("---")
    cols = st.columns(4)
    with cols[0]: st.markdown(f"<small><b>Current Price:</b> ${st.session_state.live_price:.2f}</small>", unsafe_allow_html=True)
    with cols[1]: st.markdown("<small><b>Today's High:</b> $2001.00</small>", unsafe_allow_html=True)
    with cols[2]: st.markdown("<small><b>Today's Low:</b> $1948.00</small>", unsafe_allow_html=True)
    with cols[3]: st.markdown("<small><b>24h Change:</b> +1.25%</small>", unsafe_allow_html=True)
    st.markdown("---")

# --- Top Row ---
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

    # --- Stylish Refresh Button ---
    refresh = st.markdown("""
        <style>
        div.stButton > button {
            background-color: #1e88e5;
            color: white;
            font-weight: bold;
            padding: 0.6em 1em;
            border-radius: 8px;
            margin-bottom: 10px;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #1669bb;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("🔄 Refresh Signal"):
        st.session_state.active_signal = generate_signal()
        st.experimental_rerun()

    signal = st.session_state.active_signal
    volume_pct = (signal["volume"] / signal["max_volume"]) * 100
    icon = "🔴" if signal["type"] == "SELL" else "🟢" if signal["type"] == "BUY" else "⚪"
    st.markdown(f"#### {icon} {signal['type']} Recommendation")
    st.markdown(f"<small><b>Entry Price:</b> {signal['entry']}</small>", unsafe_allow_html=True)
    st.markdown(f"<small><b>Take Profit:</b> {signal['tp']}</small>", unsafe_allow_html=True)
    st.markdown(f"<small><b>Stop Loss:</b> {signal['sl']}</small>", unsafe_allow_html=True)
    st.markdown(f"<small><b>Volume:</b> {signal['volume']:,} ({volume_pct:.1f}%)</small>", unsafe_allow_html=True)
    st.progress(signal["strength"], text="Signal Strength")

    stochastic_pct = min(100, max(0, signal["strength"] + random.randint(-15, 15)))
    atr_pct = min(100, max(0, 100 - abs(signal["strength"] - 70) + random.randint(-10, 10)))

    st.markdown("**Complementary Indicator Confidence:**")
    st.markdown(f"<small><b>Stochastic Oscillator Match:</b> {stochastic_pct:.1f}%</small>", unsafe_allow_html=True)
    st.progress(stochastic_pct, text="Stochastic Confidence")

    st.markdown(f"<small><b>ATR Volatility Context:</b> {atr_pct:.1f}%</small>", unsafe_allow_html=True)
    st.progress(atr_pct, text="ATR Confidence")

# --- Middle Row ---
with middle_row[0]:
    st.markdown("<h5>🧠 Technical Summary</h5>", unsafe_allow_html=True)
    summary_df = pd.DataFrame(get_static_technical_summary())
    st.dataframe(summary_df, use_container_width=True, height=300)

with middle_row[1]:
    st.markdown("<h5>🕒 Signal History</h5>", unsafe_allow_html=True)
    pip_moves = []
    for i in range(1, len(signals)-1):
        e1 = signals[i]["entry"]
        e2 = signals[i+1]["entry"]
        pip_moves.append(abs(e1 - e2)*10 if e1 and e2 else "-")
    pip_moves.append("-")

    history = {
        "Time": [s["time"] for s in signals[1:]],
        "Signal": ["🔴 Sell" if s["type"] == "SELL" else "🟢 Buy" if s["type"] == "BUY" else "⚪ Hold" for s in signals[1:]],
        "Price": [f"{s['entry']:.2f}" if s["entry"] else "-" for s in signals[1:]],
        "Pips to Reversal": pip_moves
    }
    st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True, height=300)

# --- Footer ---
st.caption("Demo Data • Last Updated: " + time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
