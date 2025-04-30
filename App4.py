import streamlit as st
import time
import streamlit.components.v1 as components
from rrr_calculator import show_rrr_calculator

# --- Page Config ---
st.set_page_config(page_title="XAU/USD Fibonacci App", layout="wide")

# --- Session State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "Signals"
if "selected_signal" not in st.session_state:
    st.session_state.selected_signal = None
if "live_price" not in st.session_state:
    st.session_state.update({
        "live_price": 1975.50,  # Initial mock value
        "todays_high": 2001.00,  # Mock value
        "todays_low": 1948.00,  # Mock value
        "change_pct": 1.25,  # Mock value
        "last_refresh": time.time(),
        "api_error": False
    })

# --- Navigation ---
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Signals", "RRR Calculator"])
st.session_state.page = selection

# --- Header with Live API Toggle ---
with st.container():
    cols = st.columns([4, 1])
    cols[0].markdown("<h3>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)
    
    # Toggle between mock data and live API data
    if "use_live_api" not in st.session_state:
        st.session_state.use_live_api = False  # Start with mock data

    if cols[1].button("🔄 Toggle Live API"):
        st.session_state.use_live_api = not st.session_state.use_live_api
        st.experimental_rerun()

# --- Function to simulate live API data ---
def update_market_data():
    if st.session_state.use_live_api:
        # Here we would fetch live data from the API
        st.session_state.live_price = 1980.00  # Example live value
        st.session_state.todays_high = 2005.00  # Example live value
        st.session_state.todays_low = 1950.00  # Example live value
        st.session_state.change_pct = 1.75  # Example live value
    else:
        # Mock data used when live API is not toggled
        st.session_state.live_price = 1975.50
        st.session_state.todays_high = 2001.00
        st.session_state.todays_low = 1948.00
        st.session_state.change_pct = 1.25

# --- Signals Data ---
signals = [
    {"time": "14:30", "type": "SELL", "entry": 1975.50, "tp": 1962.00, "sl": 1985.00, "volume": 18250, "max_volume": 25000, "strength": 75},
    {"time": "14:00", "type": "BUY",  "entry": 1968.20, "tp": 1980.00, "sl": 1960.00, "volume": 20000, "max_volume": 25000, "strength": 68},
    {"time": "13:30", "type": "HOLD", "entry": None,     "tp": None,    "sl": None,    "volume": 15000, "max_volume": 25000, "strength": 50},
    {"time": "13:00", "type": "SELL", "entry": 1972.80, "tp": 1960.00, "sl": 1983.00, "volume": 21000, "max_volume": 25000, "strength": 80},
    {"time": "12:30", "type": "BUY",  "entry": 1965.00, "tp": 1975.00, "sl": 1958.00, "volume": 22000, "max_volume": 25000, "strength": 77},
]

# --- Signals Page ---
if st.session_state.page == "Signals":
    update_market_data()

    # Header with RRR icon
    with st.container():
        cols = st.columns([4, 1])
        cols[0].markdown("<h3>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)
        if cols[1].button("📊 RRR Calculator", help="Open Risk/Reward Calculator"):
            st.session_state.page = "RRR Calculator"
            st.rerun()

    # Status Bar
    with st.container():
        cols = st.columns([3,1])
        cols[0].caption(f"Last update: {time.strftime('%H:%M:%S', time.localtime(st.session_state.last_refresh))}")
        if cols[1].button("🔄 Refresh"):
            update_market_data()
            st.rerun()

    # Metrics
    metric_cols = st.columns(4)
    metrics = [
        ("Current Price", f"${st.session_state.live_price:.2f}" if st.session_state.live_price else "N/A"),
        ("Today's High", f"${st.session_state.todays_high:.2f}" if st.session_state.todays_high else "N/A"),
        ("Today's Low", f"${st.session_state.todays_low:.2f}" if st.session_state.todays_low else "N/A"),
        ("24h Change", f"{st.session_state.change_pct:+.2f}%" if st.session_state.change_pct else "N/A")
    ]
    for col, (label, value) in zip(metric_cols, metrics):
        col.markdown(f"**{label}:** {value}")
    st.markdown("---")

    # Chart
    st.subheader("Live Chart")
    components.html("""<iframe src='https://s.tradingview.com/embed-widget/advanced-chart/?symbol=OANDA:XAUUSD&theme=dark' 
                   width='100%' height='420' frameborder='0'></iframe>""", height=420)

    # Signals List
    st.subheader("Signal List")
    for i, signal in enumerate(signals):
        with st.container():
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
    # Header with back button
    with st.container():
        cols = st.columns([4, 1])
        cols[0].markdown("<h3>💰 Risk/Reward Ratio Calculator</h3>", unsafe_allow_html=True)
        if cols[1].button("⬅️ Back to Signals"):
            st.session_state.page = "Signals"
            st.rerun()

    if st.session_state.selected_signal:
        show_rrr_calculator()
    else:
        st.warning("No signal selected. Please choose a signal to calculate RRR.")
