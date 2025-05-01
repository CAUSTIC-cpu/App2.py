
import streamlit as st
import time
st.markdown("Embed your chart using `st.markdown` with HTML if safe.")
from rrr_calculator import show_rrr_calculator

# --- Config ---
st.set_page_config(page_title="XAU/USD Fibonacci App", layout="wide")

# --- Session State Defaults ---
defaults = {
    "page": "Signals",
    "use_live_api": False,
    "live_price": 1972.55,
    "todays_high": 1985.30,
    "todays_low": 1964.10,
    "change_pct": 0.32,
    "last_refresh": time.time(),
    "selected_signal": None,
    "api_key": ""
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Sidebar ---
st.sidebar.title("Navigation")
st.session_state.page = st.sidebar.radio("Go to", ["Signals", "RRR Calculator"])
st.session_state.use_live_api = st.sidebar.toggle("Use Live API")

# --- Live Data Handling ---
def fetch_live_data(api_key):
    try:
        import requests
        headers = {
            "x-access-token": api_key,
            "Content-Type": "application/json"
        }
        url = "https://www.goldapi.io/api/XAU/USD"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        return {
            "live_price": float(data["price"]),
            "todays_high": float(data["high"]),
            "todays_low": float(data["low"]),
            "change_pct": float(str(data["chg_percent"]).replace('%','')),
            "last_refresh": time.time()
        }
    except Exception as e:
        st.warning(f"Live data error: {e}")
        return None

if st.session_state.use_live_api:
    if not st.session_state.api_key:
        st.session_state.api_key = st.text_input("Enter your GoldAPI Key", type="password")
    if st.session_state.api_key:
        data = fetch_live_data(st.session_state.api_key)
        if data:
            st.session_state.update(data)

# --- Top Header ---
col1, col2, col3 = st.columns([4, 1, 1])
col1.markdown("### 📈 GOLD (XAU/USD) Fibonacci Signal Scanner")
mode_label = "Live" if st.session_state.use_live_api else "Mock"
col2.metric("Mode", mode_label)
if col3.button("🔄 Refresh"):
    if st.session_state.use_live_api and st.session_state.api_key:
        data = fetch_live_data(st.session_state.api_key)
        if data:
            st.session_state.update(data)
    else:
        st.session_state.update({
            "live_price": 1972.55,
            "todays_high": 1985.30,
            "todays_low": 1964.10,
            "change_pct": 0.32,
            "last_refresh": time.time()
        })
    st.rerun()

# --- Metrics ---
metric_cols = st.columns(4)
metric_cols[0].metric("Current Price", f"${st.session_state.live_price:.2f}")
metric_cols[1].metric("Today's High", f"${st.session_state.todays_high:.2f}")
metric_cols[2].metric("Today's Low", f"${st.session_state.todays_low:.2f}")
metric_cols[3].metric("24h Change", f"{st.session_state.change_pct:+.2f}%")

# --- Chart ---
st.markdown("### TradingView Chart")
components.html("""
<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_9d409&symbol=OANDA%3AXAUUSD&interval=15&hidesidetoolbar=1&theme=dark&style=1&timezone=Etc%2FUTC&withdateranges=1&hidevolume=1&allow_symbol_change=1" width="100%" height="450" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
""", height=450)

# --- Mock Signals Data ---
signals = [
    {"time": "14:30", "type": "SELL", "entry": 1975.50, "tp": 1962.00, "sl": 1985.00, "volume": 18250, "max_volume": 25000, "strength": 75},
    {"time": "14:00", "type": "BUY",  "entry": 1968.20, "tp": 1980.00, "sl": 1960.00, "volume": 20000, "max_volume": 25000, "strength": 68},
    {"time": "13:30", "type": "HOLD", "entry": None,     "tp": None,    "sl": None,    "volume": 15000, "max_volume": 25000, "strength": 50},
    {"time": "13:00", "type": "SELL", "entry": 1972.80, "tp": 1960.00, "sl": 1983.00, "volume": 21000, "max_volume": 25000, "strength": 80},
    {"time": "12:30", "type": "BUY",  "entry": 1965.00, "tp": 1975.00, "sl": 1958.00, "volume": 22000, "max_volume": 25000, "strength": 77},
]

# --- Signal Page Layout ---
if st.session_state.page == "Signals":
    st.markdown("### Signal List")
    for i, signal in enumerate(signals):
        icon = "🔴" if signal['type'] == "SELL" else "🟢" if signal['type'] == "BUY" else "⚪"
        with st.container():
            st.markdown(f"**{icon} {signal['type']} @ {signal['entry'] or '-'}** — TP: {signal['tp']} | SL: {signal['sl']} | Strength: {signal['strength']}%")
            if st.button("📊 RRR Calculator", key=f"rrr_{i}"):
                st.session_state.selected_signal = signal
                st.session_state.page = "RRR Calculator"
                st.rerun()
            st.markdown("---")

# --- RRR Calculator ---
if st.session_state.page == "RRR Calculator":
    st.markdown("### 💰 Risk/Reward Ratio Calculator")
    if st.button("⬅️ Back to Signals"):
        st.session_state.page = "Signals"
        st.rerun()

    if st.session_state.selected_signal:
        show_rrr_calculator()
    else:
        st.warning("Please select a signal first from the Signals page.")
