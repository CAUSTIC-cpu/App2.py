

import streamlit as st
import pandas as pd
import numpy as np
import time

# App Title
st.set_page_config(page_title="Live-Fib-Market Analyser", layout="wide")
st.title("🔮 Live-Fib-Market Analyser")

# Sidebar
st.sidebar.header("RRR Calculator")
entry_price = st.sidebar.number_input("Entry Price", value=1900.0, step=0.1)
stop_loss = st.sidebar.number_input("Stop Loss", value=1895.0, step=0.1)
take_profit = st.sidebar.number_input("Take Profit", value=1910.0, step=0.1)

# RRR Calculation
if stop_loss != entry_price:
    risk = abs(entry_price - stop_loss)
    reward = abs(take_profit - entry_price)
    rrr = round(reward / risk, 2) if risk != 0 else 0
    st.sidebar.success(f"RRR: {rrr} : 1")
else:
    st.sidebar.warning("Stop Loss cannot be equal to Entry Price.")

st.divider()

# Live TradingView Chart
st.subheader("📈 Live XAU/USD Chart (Auto-refreshes every minute)")

tradingview_code = """
<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_d2e15&symbol=OANDA%3AXAUUSD&interval=1&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Africa%2FNairobi" width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
"""

st.components.v1.html(tradingview_code, height=500)

st.info("Chart auto-refreshes every minute. Please refresh the app to update manually.")

st.divider()

# 80% Strength Signals Table
st.subheader("⚡ 80% Strength Buy/Sell Signals")

# Simulated Signal Data (replace with live data logic)
np.random.seed(int(time.time()))
signals_data = pd.DataFrame({
    "Time": pd.date_range(end=pd.Timestamp.now(), periods=5, freq='T'),
    "Signal": np.random.choice(["Buy", "Sell"], 5),
    "Strength (%)": np.random.uniform(80, 100, 5).round(2),
    "Volume (%)": np.random.uniform(50, 100, 5).round(2)
})

st.table(signals_data)

st.divider()

# Previous 10 Strongest Signals Table
st.subheader("🗂️ Previous 10 Strongest Signals")

# Simulated Historical Signal Data (replace with real signal history)
history_data = pd.DataFrame({
    "Time": pd.date_range(end=pd.Timestamp.now(), periods=10, freq='2T'),
    "Signal": np.random.choice(["Buy", "Sell"], 10),
    "Strength (%)": np.random.uniform(70, 100, 10).round(2),
    "Volume (%)": np.random.uniform(40, 100, 10).round(2)
}).sort_values(by="Strength (%)", ascending=False)

st.table(history_data)
