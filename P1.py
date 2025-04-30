import streamlit as st

st.set_page_config(page_title="RRR Calculator", page_icon="📈", layout="centered")

st.title("📊 Risk-Reward Ratio (RRR) Calculator")

# Input fields with icons
entry_price = st.number_input("💰 Entry Price", min_value=0.0, format="%.2f")
stop_loss = st.number_input("❌ Stop Loss", min_value=0.0, format="%.2f")
take_profit = st.number_input("✅ Take Profit", min_value=0.0, format="%.2f")

# Validation and calculation
if entry_price and stop_loss and take_profit:
    risk = abs(entry_price - stop_loss)
    reward = abs(take_profit - entry_price)
    if risk == 0:
        st.warning("Stop Loss and Entry Price cannot be the same.")
    else:
        rrr = reward / risk
        color = "green" if rrr >= 2 else "orange" if rrr >= 1 else "red"
        st.markdown(f"### RRR: <span style='color:{color}; font-size: 24px;'>{rrr:.2f}</span>", unsafe_allow_html=True)

        st.caption("Ideal RRR is 2.0 or higher for strong trade setups.")

else:
    st.info("Enter values above to calculate your RRR.")
