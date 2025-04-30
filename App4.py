import streamlit as st
from rrr_calculator import show_rrr_calculator
import pandas as pd
import streamlit.components.v1 as components
import time
import requests

# --- Page Config ---
st.set_page_config(page_title="XAU/USD Fibonacci App", layout="wide")

# --- API Configuration ---
if "GOLDAPI_API_KEY" not in st.secrets:
    st.error("❌ Missing API key in secrets.toml. Please configure your GoldAPI credentials.")
    st.stop()

API_KEY = st.secrets["GOLDAPI_API_KEY"]
SYMBOL = "XAUUSD"
HEADERS = {"X-API-KEY": API_KEY}
BASE_URL = f"https://www.goldapi.io/api/{SYMBOL}/USD"

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "Signals"
if "selected_signal" not in st.session_state:
    st.session_state.selected_signal = None

# Initialize with API data
if "live_price" not in st.session_state:
    st.session_state.update({
        "live_price": None,
        "todays_high": None,
        "todays_low": None,
        "change_pct": None,
        "last_refresh": time.time(),
        "api_error": False
    })

# --- API Functions ---
@st.cache_data(ttl=60, show_spinner=False)
def fetch_gold_price():
    """Fetch gold price data with error handling and rate limiting"""
    try:
        response = requests.get(BASE_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        # Debug: Uncomment to see API response structure
        # print("API Response:", data)

        return {
            "price": float(data.get("price", 0)),
            "high": float(data.get("high", 0)),
            "low": float(data.get("low", 0)),
            "change_pct": float(str(data.get("change_pct", 0)).replace('%', '')),
            "timestamp": time.time()
        }
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            st.error("⚠️ API rate limit exceeded. Please wait before refreshing.")
            st.session_state.last_refresh = time.time() + 300  # 5 min cooldown
        else:
            st.error(f"API Error: {e.response.status_code} - {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

# --- Data Refresh Logic ---
def update_market_data():
    """Handle data refresh with error state management"""
    fresh_data = fetch_gold_price()
    
    if fresh_data:
        st.session_state.update({
            "live_price": fresh_data["price"],
            "todays_high": fresh_data["high"],
            "todays_low": fresh_data["low"],
            "change_pct": fresh_data["change_pct"],
            "last_refresh": fresh_data["timestamp"],
            "api_error": False
        })
    else:
        st.session_state.api_error = True

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
    # Initial data load
    if st.session_state.live_price is None:
        update_market_data()

    st.markdown("<h3>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)
    
    # Refresh controls
    with st.container():
        cols = st.columns([3,1])
        with cols[0]:
            st.caption(f"Last update: {time.strftime('%H:%M:%S', time.localtime(st.session_state.last_refresh))}")
        with cols[1]:
            if st.button("🔄 Manual Refresh", help="Force immediate data refresh"):
                update_market_data()
                st.rerun()

    # Live stats
    with st.container():
        cols = st.columns(4)
        metrics = [
            ("Current Price", f"${st.session_state.live_price:.2f}" if st.session_state.live_price else "N/A"),
            ("Today's High", f"${st.session_state.todays_high:.2f}" if st.session_state.todays_high else "N/A"),
            ("Today's Low", f"${st.session_state.todays_low:.2f}" if st.session_state.todays_low else "N/A"),
            ("24h Change", 
             f"{st.session_state.change_pct:+.2f}%" if st.session_state.change_pct is not None else "N/A")
        ]
        
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.markdown(f"**{label}:** {value}")
        st.markdown("---")

    # Chart display
    st.subheader("Live Chart")
    tv_chart = """
    <iframe src='https://s.tradingview.com/embed-widget/advanced-chart/?symbol=OANDA:XAUUSD&theme=dark' 
            width='100%' height='420' frameborder='0'></iframe>
    """
    components.html(tv_chart, height=420)

    # Signal list
    st.subheader("Signal List")
    for i, signal in enumerate(signals):
        with st.container():
            icon = "🔴" if signal['type'] == "SELL" else "🟢" if signal['type'] == "BUY" else "⚪"
            entry = f"@ {signal['entry']}" if signal['entry'] else ""
            st.markdown(f"### {icon} {signal['type']} {entry}")
            
            cols = st.columns([3,1])
            with cols[0]:
                st.write(f"**TP**: {signal['tp']}, **SL**: {signal['sl']}, **Strength**: {signal['strength']}%")
            with cols[1]:
                if st.button(f"📊 Calculate RRR", key=f"btn_{i}"):
                    st.session_state.selected_signal = signal
                    st.session_state.page = "RRR Calculator"
                    st.rerun()
            st.markdown("---")

# --- RRR Calculator Page ---
elif st.session_state.page == "RRR Calculator":
    if st.session_state.selected_signal:
        show_rrr_calculator()
    else:
        st.warning("Please select a signal first from the Signals page.")
    if st.button("⬅️ Back to Signals"):
        st.session_state.page = "Signals"
        st.rerun()

# --- Auto-Refresh Logic ---
if st.session_state.page == "Signals" and not st.session_state.api_error:
    elapsed = time.time() - st.session_state.last_refresh
    if elapsed > 60:  # Refresh every 60 seconds
        with st.spinner("Updating market data..."):
            update_market_data()
            st.rerun()
