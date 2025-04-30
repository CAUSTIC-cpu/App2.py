import streamlit as st
from rrr_calculator import show_rrr_calculator
import pandas as pd
import streamlit.components.v1 as components
import time
import requests

# --- Page Config ---
st.set_page_config(page_title="XAU/USD Fibonacci App", layout="wide")

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "Signals"
if "selected_signal" not in st.session_state:
    st.session_state.selected_signal = None
if "live_price" not in st.session_state:
    st.session_state.live_price = 1975.50
if "todays_high" not in st.session_state:
    st.session_state.todays_high = 2001.00
if "todays_low" not in st.session_state:
    st.session_state.todays_low = 1948.00
if "change_pct" not in st.session_state:
    st.session_state.change_pct = +1.25

# --- GoldAPI Configuration ---
API_KEY = "goldapi-6j5sma3qfw4a-io"
SYMBOL = "XAUUSD"
HEADERS = {
    "x-access-token": API_KEY,
    "Content-Type": "application/json"
}

def fetch_gold_price():
    try:
        response = requests.get(f"https://www.goldapi.io/api/{SYMBOL}", headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        st.session_state.live_price = data.get('price', st.session_state.live_price)
        st.session_state.todays_high = data.get('high', st.session_state.todays_high)
        st.session_state.todays_low = data.get('low', st.session_state.todays_low)
        st.session_state.change_pct = data.get('change_pct', st.session_state.change_pct)
        
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        # Keep previous values if API call fails

# --- Navigation ---
st.sidebar.title("Navigation")
tabs = ["Signals", "RRR Calculator"]
selection = st.sidebar.radio("Go to", tabs)
st.session_state.page = selection

# --- Static Signals ---
signals = [
    {"time": "14:30", "type": "SELL", "entry": 1975.50, "tp": 1962.00, "sl": 1985.00, "volume": 18250, "max_volume": 25000, "strength": 75},
    {"time": "14:00", "type": "BUY",  "entry": 1968.20, "tp": 1980.00, "sl": 1960.00, "volume": 20000, "max_volume": 25000, "strength": 68},
    {"time": "13:30", "type": "HOLD", "entry": None,     "tp": None,    "sl": None,    "volume": 15000, "max_volume": 25000, "strength": 50},
    {"time": "13:00", "type": "SELL", "entry": 1972.80, "tp": 1960.00, "sl": 1983.00, "volume": 21000, "max_volume": 25000, "strength": 80},
    {"time": "12:30", "type": "BUY",  "entry": 1965.00, "tp": 1975.00, "sl": 1958.00, "volume": 22000, "max_volume": 25000, "strength": 77},
]

# --- Signals Page ---
if st.session_state.page == "Signals":
    st.markdown("<h3>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)

    # Live stats
    cols = st.columns(4)
    with cols[0]: st.markdown(f"**Current Price:** ${st.session_state.live_price:.2f}")
    with cols[1]: st.markdown(f"**Today's High:** ${st.session_state.todays_high:.2f}")
    with cols[2]: st.markdown(f"**Today's Low:** ${st.session_state.todays_low:.2f}")
    with cols[3]: st.markdown(f"**24h Change:** {st.session_state.change_pct:.2f}%")
    st.markdown("---")

    st.subheader("Live Chart")
    tv_chart = """
    <iframe src='https://s.tradingview.com/embed-widget/advanced-chart/?symbol=OANDA:XAUUSD&theme=dark' 
            width='100%' height='420' frameborder='0'></iframe>
    """
    components.html(tv_chart, height=420)

    st.subheader("Signal List")
    for i, signal in enumerate(signals):
        with st.container():
            icon = "🔴" if signal['type'] == "SELL" else "🟢" if signal['type'] == "BUY" else "⚪"
            st.markdown(f"### {icon} {signal['type']} @ {signal['entry'] if signal['entry'] else '-'}")
            st.write(f"**TP**: {signal['tp']}, **SL**: {signal['sl']}, **Strength**: {signal['strength']}%")
            if st.button(f"📊 Calculate RRR", key=f"btn{i}"):
                st.session_state.selected_signal = signal
                st.session_state.page = "RRR Calculator"
                st.experimental_rerun()

# --- RRR Calculator Page ---
elif st.session_state.page == "RRR Calculator":
    if st.session_state.selected_signal:
        show_rrr_calculator()
    else:
        st.warning("Please select a signal first from the Signals page.")

# --- Auto Refresh Logic ---
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 60:
    try:
        fetch_gold_price()
        st.session_state.last_refresh = time.time()
        st.rerun()
    except Exception as e:
        st.error(f"Auto-refresh failed: {str(e)}")
