import pandas as pd
import streamlit as st
import time
import random

# --- App Configuration ---
st.set_page_config(page_title="XAUUSD Fibonacci Scanner", layout="wide")

# --- Session State ---
if "show_rrr" not in st.session_state:
    st.session_state.show_rrr = False
if "live_price" not in st.session_state:
    st.session_state.live_price = 1975.50

# --- Live Price Simulation ---
def update_live_price():
    st.session_state.live_price += random.uniform(-0.5, 0.5)
    st.session_state.live_price = round(st.session_state.live_price, 2)

# --- Toggle RRR Section ---
def toggle_rrr():
    st.session_state.show_rrr = not st.session_state.show_rrr

# --- Main Content ---
st.markdown("<h3 style='margin-bottom: 0;'>📈 GOLD (XAU/USD) Fibonacci Signal Scanner</h3>", unsafe_allow_html=True)

# --- RRR Button ---
st.button("⚖️ R.R.R", on_click=toggle_rrr, help="Click to toggle Risk/Reward Calculator")

# --- RRR Section ---
if st.session_state.show_rrr:
    st.markdown("<h4 style='margin-top: 10px;'>Risk/Reward Ratio (AB:CD Structure)</h4>", unsafe_allow_html=True)

    with st.form("rrr_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            entry_price = st.number_input("Entry Price", value=st.session_state.live_price)
        with col2:
            stop_loss = st.number_input("Stop Loss", value=st.session_state.live_price - 5.0)
        with col3:
            take_profit = st.number_input("Take Profit", value=st.session_state.live_price + 10.0)
        trade_size = st.number_input("Lot Size", value=1.0, min_value=0.1, step=0.1)
        submitted = st.form_submit_button("Calculate")

    if submitted:
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)

        if risk + reward == 0:
            st.error("Risk and reward cannot both be zero.")
        else:
            ab = int((risk / (risk + reward)) * 100)
            cd = int((reward / (risk + reward)) * 100)
            pip_value = 100
            profit = reward * pip_value * trade_size
            loss = risk * pip_value * trade_size

            st.markdown(f"<h5 style='color:#FFA500;'>AB:CD = {ab}:{cd}</h5>", unsafe_allow_html=True)

            # Visual bar
            st.markdown(f"""
            <div style="background: #1e1e1e; border-radius: 10px; padding: 5px; margin-bottom: 10px;">
                <div style="width: {ab}%; background: #ff4b4b;
                    height: 25px; border-radius: 5px 0 0 5px;
                    display: inline-block; text-align: center; color: white;">RISK {ab}%</div>
                <div style="width: {cd}%; background: #4CAF50;
                    height: 25px; border-radius: 0 5px 5px 0;
                    display: inline-block; text-align: center; color: white;">REWARD {cd}%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="margin-top: 10px;">
                <span style="padding: 8px 16px; background: #4CAF5050; border-radius: 5px; margin-right: 15px;">
                    📈 Potential Profit: <strong style="color:#4CAF50;">${profit:,.2f}</strong>
                </span>
                <span style="padding: 8px 16px; background: #ff4b4b50; border-radius: 5px;">
                    📉 Potential Loss: <strong style="color:#ff4b4b;">${loss:,.2f}</strong>
                </span>
            </div>
            """, unsafe_allow_html=True)

# --- Placeholder for other signals, chart, or history ---
st.markdown("---")
st.caption(f"Demo Data • Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")

# --- Auto-refresh logic every 60s ---
if time.time() - st.session_state.get("last_refresh", 0) > 60:
    update_live_price()
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()
