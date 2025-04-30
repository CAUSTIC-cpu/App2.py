import streamlit as st

# Simulated selected signal (replace with actual signal data)
selected_signal = {
    "direction": "Buy",  # or "Sell"
    "entry": 2300.00,
    "stop_loss": 2285.00,
    "take_profit": 2330.00,
}

# --- UI HEADER ---
st.set_page_config(page_title="XAU/USD RRR", page_icon="📈", layout="centered")
st.markdown("## 🔄 Risk-Reward Calculator for Selected Signal")

# --- BACK BUTTON ---
if st.button("⬅️ Back to Signals"):
    st.session_state.page = "signals"  # Simulated page switch (you control this logic in your app)

# --- PRE-FILLED FIELDS ---
entry_price = st.number_input("💰 Entry Price", value=selected_signal["entry"], format="%.2f")
stop_loss = st.number_input("❌ Stop Loss", value=selected_signal["stop_loss"], format="%.2f")
take_profit = st.number_input("✅ Take Profit", value=selected_signal["take_profit"], format="%.2f")

# --- RRR and % Calculation ---
if entry_price and stop_loss and take_profit:
    risk = abs(entry_price - stop_loss)
    reward = abs(take_profit - entry_price)

    if risk == 0:
        st.warning("Stop Loss and Entry cannot be equal.")
    else:
        rrr = reward / risk

        # Risk and Reward as % of Entry Price (Base = 100%)
        risk_pct = (risk / entry_price) * 100
        reward_pct = (reward / entry_price) * 100

        color = "green" if rrr >= 2 else "orange" if rrr >= 1 else "red"
        st.markdown(
            f"""
            ### Risk : Reward
            <span style='font-size:20px; color:{color};'>
            {risk_pct:.2f}% : {reward_pct:.2f}%<br>
            RRR = {rrr:.2f}
            </span>
            """,
            unsafe_allow_html=True
        )
        st.caption("A reward of ≥ 200% of risk (RRR ≥ 2.0) is ideal.")
else:
    st.info("Fill in all fields to compute risk and reward.")
