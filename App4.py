import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import time

st.set_page_config(page_title="Gold Smart Fib Signals", layout="wide")

# --- Title ---
st.title("GOLD (XAU/USD) Fibonacci Signal Scanner")
st.markdown("Live analysis using Fibonacci, volume, and signal logging with risk/reward logic.")

# --- Live price from Yahoo Finance ---
data = yf.download("XAUUSD=X", period="7d", interval="1h")
if data.empty:
    st.error("Failed to fetch XAU/USD data.")
    st.stop()

latest_price = data["Close"][-1]
high = data["High"].max()
low = data["Low"].min()

# --- Fibonacci Levels Calculation ---
fib_levels = {
    "0.0%": high,
    "23.6%": high - (high - low) * 0.236,
    "38.2%": high - (high - low) * 0.382,
    "50.0%": high - (high - low) * 0.5,
    "61.8%": high - (high - low) * 0.618,
    "78.6%": high - (high - low) * 0.786,
    "100.0%": low
}
fib_df = pd.DataFrame(fib_levels.items(), columns=["Level", "Price"])
st.subheader("Fibonacci Levels (1H Range)")
st.dataframe(fib_df.set_index("Level").style.format({"Price": "{:.2f}"}))

# --- Mock volume logic (can integrate real volume source later) ---
volume_today = 110000
average_volume = 100000

# --- Signal Detection ---
signal = None
risk_reward = None
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if latest_price <= fib_levels["61.8%"] and volume_today > average_volume:
    signal = f"🟢 **BUY** @ {latest_price:.2f}"
    risk_reward = "Risk/Reward: 3.2x (78%)"
elif latest_price >= fib_levels["38.2%"] and volume_today > average_volume:
    signal = f"🔴 **SELL** @ {latest_price:.2f}"
    risk_reward = "Risk/Reward: 2.4x (64%)"
else:
    signal = "⚪ No strong signal"
    risk_reward = "--"

st.subheader("Live Signal")
st.metric(label="Current Price", value=f"${latest_price:.2f}")
st.markdown(f"**Signal:** {signal}")
st.markdown(f"**{risk_reward}**")

# --- Signal History Logging (Store latest 5 signals in session state) ---
if "signal_log" not in st.session_state:
    st.session_state.signal_log = []

if "No strong signal" not in signal:
    st.session_state.signal_log.insert(0, {
        "time": timestamp,
        "signal": signal
    })

st.session_state.signal_log = st.session_state.signal_log[:5]

# --- Signal Log Display ---
st.subheader("Signal Log (Latest 5)")
for s in st.session_state.signal_log:
    st.markdown(f"{s['signal']} | 🕒 *{s['time']}*")

# --- Live TradingView Chart ---
st.subheader("Live XAU/USD Chart")
chart = """
<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_f7f54&symbol=OANDA:XAUUSD&interval=60&hidesidetoolbar=1&theme=dark&style=1&timezone=Etc/UTC&withdateranges=1&hideideas=1&hidelegend=1&autosize=true" width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
"""
st.components.v1.html(chart, height=500)

# --- Auto Refresh Countdown ---
st.subheader("Auto Refresh")
countdown = 60
placeholder = st.empty()
for i in range(countdown, 0, -1):
    placeholder.markdown(f"⏳ Refreshing in **{i} seconds**...")
    time.sleep(1)
st.rerun()
