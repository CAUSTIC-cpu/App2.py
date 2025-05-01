import streamlit as st

def show_rrr_calculator():
    st.subheader("Risk/Reward Ratio Calculator")

    col1, col2 = st.columns(2)

    with col1:
        entry = st.number_input("Entry Price", value=1975.00, format="%.2f")
        sl = st.number_input("Stop Loss", value=1965.00, format="%.2f")

    with col2:
        tp = st.number_input("Take Profit", value=1990.00, format="%.2f")
        risk_amount = st.number_input("Risk Amount ($)", value=100.0)

    if entry and sl and tp and sl != tp:
        risk = abs(entry - sl)
        reward = abs(tp - entry)
        rrr = reward / risk if risk != 0 else 0
        potential_reward = rrr * risk_amount

        st.markdown(f"**Risk/Reward Ratio:** `{rrr:.2f}`")
        st.markdown(f"**Potential Reward:** `${potential_reward:.2f}`")
    else:
        st.warning("Please input valid Entry, Stop Loss, and Take Profit values.")
