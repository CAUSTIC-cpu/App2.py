import streamlit as st

def show_rrr_calculator():
    st.title("🔄 RRR Calculator")

    # Back button
    if st.button("⬅️ Back to Signals"):
        st.session_state.page = "signals"
        return

    signal = st.session_state.get("selected_signal", {})

    entry_price = st.number_input("💰 Entry Price", value=signal.get("entry", 0.0), format="%.2f")
    stop_loss = st.number_input("❌ Stop Loss", value=signal.get("stop_loss", 0.0), format="%.2f")
    take_profit = st.number_input("✅ Take Profit", value=signal.get("take_profit", 0.0), format="%.2f")

    if entry_price and stop_loss and take_profit:
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)

        if risk == 0:
            st.warning("Risk cannot be zero.")
        else:
            rrr = reward / risk
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
