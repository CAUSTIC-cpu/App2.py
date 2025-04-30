import streamlit as st
from rrr_calculator import show_rrr_calculator

# Page setup
st.set_page_config(page_title="XAU/USD Signal App", layout="centered")

# --- Initialize session state for navigation and signal data ---
if "page" not in st.session_state:
    st.session_state.page = "signals"

if "selected_signal" not in st.session_state:
    st.session_state.selected_signal = None

# --- Main Navigation ---
if st.session_state.page == "signals":
    st.title("📌 XAU/USD Fibonacci Signals")

    # Sample list of signals (replace with your real data)
    sample_signals = [
        {
            "id": 1,
            "direction": "Buy",
            "entry": 2300.00,
            "stop_loss": 2285.00,
            "take_profit": 2330.00,
        },
        {
            "id": 2,
            "direction": "Sell",
            "entry": 2320.00,
            "stop_loss": 2335.00,
            "take_profit": 2290.00,
        }
    ]

    # Display signals
    for signal in sample_signals:
        with st.container():
            st.markdown(f"### Signal #{signal['id']} - {signal['direction']}")
            st.write(f"**Entry**: {signal['entry']} | **SL**: {signal['stop_loss']} | **TP**: {signal['take_profit']}")
            if st.button(f"📊 View RRR for Signal #{signal['id']}", key=signal['id']):
                st.session_state.selected_signal = signal
                st.session_state.page = "rrr"
                st.experimental_rerun()  # force rerun to navigate immediately

elif st.session_state.page == "rrr":
    show_rrr_calculator()
