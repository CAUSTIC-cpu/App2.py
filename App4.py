import streamlit as st
import time
import random
from rrr_calculator import show_rrr_calculator

# --- Page Config ---
st.set_page_config(page_title="XAU/USD Fibonacci App", layout="wide")

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "Signals"
if "selected_signal" not in st.session_state:
    st.session_state.selected_signal = None
if "use_live_api" not in st.session_state:
    st.session_state.use_live_api = False
if "live_data" not in st.session_state:
    st.session_state.live_data = {
        "price": 1975.00,
        "high": 1985.00,
        "low": 1960.00,
        "change_pct": 0.35,
        "last_refresh": time.time()
    }

# --- API Call (only if using live) ---
def fetch_live_gold_price(api_key: str):
    import requests
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    url = "https://www.goldapi.io/api/XAU/USD"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {
            "price": float(data.get("price", 0)),
            "high": float(data.get("high", 0)),
            "low": float(data.get("low", 0)),
            "change_pct": float(str(data.get("chg_percent", 0)).replace('%', '')),
            "last_refresh": time.time()
        }
    except Exception as e:
        st.warning(f"Failed to fetch live data: {e}")
        return None

# --- Mock Data Refresh ---
def generate_mock_data():
    return {
        "price": round(random.uniform(1960, 1980), 2),
        "high": 1985.00,
        "low": 1960.00,
        "change_pct": round(random.uniform(-1.5, 1.5), 2),
        "last_refresh": time.time()
    }

# --- Update Data Function ---
def update_data():
    if st.session_state.use_live_api:
        api_key = st.text_input("Enter GoldAPI Key", type="password")
        if api_key:
            data = fetch_live_gold_price(api_key)
            if data:
                st.session_state.live_data = data
    else:
        st.session_state.live_data = generate_mock_data()

# --- Navigation Sidebar ---
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Signals", "RRR Calculator"])
st.session_state.page = selection

# --- Sample Signals ---
signals = [
    {"time": "14:30", "type": "SELL", "entry": 1975.5, "tp": 1962.0, "sl": 1985.0, "strength": 75},
    {"time": "14:00", "type": "BUY",  "entry": 1968.2, "tp": 1980.0, "sl": 1960.0, "strength": 68},
    {"time": "13:30", "type": "HOLD", "entry": None,   "tp": None,   "sl": None,   "strength": 50},
]

# --- Signals Page ---
if st.session_state.page == "Signals":
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown("### 📈 XAU/USD Fibonacci Signal Scanner")
        toggle = col2.toggle("Use Live API", value=st.session_state.use_live_api)
        if toggle != st.session_state.use_live_api:
            st.session_state.use_live_api = toggle
            st.rerun()
        if col3.button("📊 RRR Calculator"):
            st.session_state.page = "RRR Calculator"
            st.rerun()

    update_data()
    data = st.session_state.live_data

    # Price Metrics
    cols = st.columns(4)
    cols[0].metric("Current Price", f"${data['price']:.2f}")
    cols[1].metric("High", f"${data['high']:.2f}")
    cols[2].metric("Low", f"${data['low']:.2f}")
    cols[3].metric("Change %", f"{data['change_pct']:+.2f}%")
    st.caption(f"Last updated: {time.strftime('%H:%M:%S', time.localtime(data['last_refresh']))}")
    st.markdown("---")

    # Signal Display
    for i, signal in enumerate(signals):
        icon = "🔴" if signal["type"] == "SELL" else "🟢" if signal["type"] == "BUY" else "⚪"
        st.markdown(f"### {icon} {signal['type']} @ {signal['entry'] or '-'}")
        st.write(f"**TP:** {signal['tp']} | **SL:** {signal['sl']} | **Strength:** {signal['strength']}%")
        if st.button("📊 Calculate RRR", key=f"calc_{i}"):
            st.session_state.selected_signal = signal
            st.session_state.page = "RRR Calculator"
            st.rerun()
        st.markdown("---")

# --- RRR Calculator Page ---
elif st.session_state.page == "RRR Calculator":
    col1, col2 = st.columns([4, 1])
    col1.markdown("### 💰 Risk/Reward Calculator")
    if col2.button("⬅️ Back"):
        st.session_state.page = "Signals"
        st.rerun()

    if st.session_state.selected_signal:
        show_rrr_calculator()
    else:
        st.info("No signal selected. Please choose a signal from the Signals page.")
