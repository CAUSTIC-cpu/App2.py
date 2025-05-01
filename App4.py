import streamlit as st
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="XAU/USD Fibonacci App", layout="wide")

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "Signals"
if "selected_signal" not in st.session_state:
    st.session_state.selected_signal = None
if "use_live_api" not in st.session_state:
    st.session_state.use_live_api = False
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""
if "live_price" not in st.session_state:
    st.session_state.update({
        "live_price": 1975.50,
        "todays_high": 2001.00,
        "todays_low": 1948.00,
        "change_pct": 1.25,
        "last_refresh": time.time(),
        "api_error": False
    })

# --- Function to Update Market Data ---
def update_market_data():
    if st.session_state.use_live_api:
        if not st.session_state.user_api_key:
            st.warning("Please enter your GoldAPI key in the sidebar to use Live API data.")
            return
        headers = {
            "x-access-token": st.session_state.user_api_key,
            "Content-Type": "application/json"
        }
        try:
            response = requests.get("https://www.goldapi.io/api/XAU/USD", headers=headers)
            response.raise_for_status()
            data = response.json()
            st.session_state.update({
                "live_price": float(data.get("price", 0)),
                "todays_high": float(data.get("high", 0)),
                "todays_low": float(data.get("low", 0)),
                "change_pct": float(str(data.get("chgpct", 0)).replace('%', '')),
                "last_refresh": time.time(),
                "api_error": False
            })
        except requests.exceptions.RequestException as e:
            st.session_state.api_error = True
            st.error(f"API Request Failed: {e}")
    else:
        # Use mock data
        st.session_state.update({
            "live_price": 1975.50,
            "todays_high": 2001.00,
            "todays_low": 1948.00,
            "change_pct": 1.25,
            "last_refresh": time.time(),
            "api_error": False
        })

# --- Sidebar for Navigation & API ---
st.sidebar.title("Navigation")
st.session_state.page = st.sidebar.radio("Go to", ["Signals", "RRR Calculator"])

st.sidebar.markdown("### Settings")
st.session_state.use_live_api = st.sidebar.checkbox("Use Live API", value=st.session_state.use_live_api)
if st.session_state.use_live_api:
    st.session_state.user_api_key = st.sidebar.text_input("Enter GoldAPI Key", type="password")

# --- Signals Mock Data ---
signals = [
    {"time": "14:30", "type": "SELL", "entry": 1975.50, "tp": 1962.00, "sl": 1985.00, "volume": 18250, "max_volume": 25000, "strength": 75},
    {"time": "14:00", "type": "BUY",  "entry": 1968.20, "tp": 1980.00, "sl": 1960.00, "volume": 20000, "max_volume": 25000, "strength": 68},
    {"time": "13:30", "type": "HOLD", "entry": None,     "tp": None,    "sl": None,    "volume": 15000, "max_volume": 25000, "strength": 50},
    {"time": "13:00", "type": "SELL", "entry": 1972.80, "tp": 1960.00, "sl": 1983.00, "volume": 21000, "max_volume": 25000, "strength": 80},
    {"time": "12:30", "type": "BUY",  "entry": 1965.00, "tp": 1975.00, "sl": 1958.00, "volume": 22000, "max_volume": 25000, "strength": 77},
]

# --- Main UI ---
if st.session_state.page == "Signals":
    update_market_data()

    # Header
    st.markdown("## 📈 XAU/USD Fibonacci Signal Scanner")

    # Status Bar
    cols = st.columns([3,1])
    cols[0].caption(f"Last update: {time.strftime('%H:%M:%S', time.localtime(st.session_state.last_refresh))}")
    if cols[1].button("🔄 Refresh"):
        update_market_data()
        st.rerun()

    # Market Metrics
    metric_cols = st.columns(4)
    metric_cols[0].metric("Current Price", f"${st.session_state.live_price:.2f}")
    metric_cols[1].metric("Today's High", f"${st.session_state.todays_high:.2f}")
    metric_cols[2].metric("Today's Low", f"${st.session_state.todays_low:.2f}")
    metric_cols[3].metric("24h Change", f"{st.session_state.change_pct:+.2f}%")

    st.markdown("---")

    # Signals List
    st.subheader("Signal List")
    for i, signal in enumerate(signals):
        icon = "🔴" if signal['type'] == "SELL" else "🟢" if signal['type'] == "BUY" else "⚪"
        st.markdown(f"### {icon} {signal['type']} @ {signal['entry'] or '-'}")
        cols = st.columns([3,1])
        cols[0].write(f"**TP:** {signal['tp']} | **SL:** {signal['sl']} | **Strength:** {signal['strength']}%")
        if cols[1].button("📊 Calculate RRR", key=f"btn_{i}"):
            st.session_state.selected_signal = signal
            st.session_state.page = "RRR Calculator"
            st.rerun()
        st.markdown("---")

# --- RRR Calculator Page ---
elif st.session_state.page == "RRR Calculator":
    st.markdown("## 💰 Risk/Reward Ratio Calculator")
    if st.button("⬅️ Back to Signals"):
        st.session_state.page = "Signals"
        st.rerun()

    if st.session_state.selected_signal:
        # Call your RRR calculator function
        from rrr_calculator import show_rrr_calculator
        show_rrr_calculator()
    else:
        st.warning("No signal selected. Please choose one from the signals page.")
