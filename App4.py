import pandas as pd
import streamlit as st
from datetime import timedelta

# --- Streamlit Config ---
st.set_page_config(page_title="XAUUSD Fibonacci Demo", layout="wide")
st.title("GOLD (XAU/USD) Fibonacci Signal Scanner (Demo)")

# --- Static Data Generation ---
@st.cache_data
def get_static_data():
    base_price = 1950.00
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq="H")
    
    return pd.DataFrame({
        "Time": dates,
        "Open": [base_price + i*0.5 for i in range(100)],
        "High": [base_price + i*0.5 + 2.5 for i in range(100)],
        "Low": [base_price + i*0.5 - 2.0 for i in range(100)],
        "Close": [base_price + i*0.5 + 0.3 for i in range(100)],
        "Volume": [100000 + i*500 for i in range(100)]
    }).sort_values("Time")

df = get_static_data()

# --- Fibonacci Calculation ---
high = df["High"].max()
low = df["Low"].min()

levels = {
    "0.0%": high,
    "23.6%": high - (high - low) * 0.236,
    "38.2%": high - (high - low) * 0.382,
    "50.0%": high - (high - low) * 0.5,
    "61.8%": high - (high - low) * 0.618,
    "78.6%": high - (high - low) * 0.786,
    "100.0%": low,
}

# --- NEW: Mock Signal History Data ---
def generate_mock_history():
    base_time = df["Time"].iloc[-1]
    return pd.DataFrame([
        {"Time": base_time - timedelta(hours=4), "Price": 1968.20, "Type": "BUY"},
        {"Time": base_time - timedelta(hours=3), "Price": 1972.80, "Type": "SELL"},
        {"Time": base_time - timedelta(hours=2), "Price": 1975.50, "Type": "SELL"},
        {"Time": base_time - timedelta(hours=1), "Price": 1971.30, "Type": "BUY"},
        {"Time": base_time, "Price": 1975.50, "Type": "SELL"}
    ])

history_df = generate_mock_history()

# --- Display Sections ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fibonacci Levels (Demo Data)")
    fib_df = pd.DataFrame(levels.items(), columns=["Level", "Price"])
    st.dataframe(fib_df.set_index("Level").style.format({"Price": "{:.2f}"}))
    
    st.subheader("Demo Signal")
    st.metric(label="Current Price", value="$1975.50")
    st.markdown("**Signal:** 🔴 **SELL** @ 1975.50")
    st.markdown("**Risk/Reward:** 2.2x (60%)")

with col2:
    st.subheader("Signal History")
    st.dataframe(
        history_df.style.format({
            "Price": "${:.2f}",
            "Time": lambda x: x.strftime("%Y-%m-%d %H:%M")
        }).apply(lambda row: [
            f"color: {'#4CAF50' if row.Type=='BUY' else '#FF5252'}"
            for _ in row], axis=1),
        height=400
    )

# --- Existing Signal Log ---
st.subheader("Signal Log (Demo)")
demo_log = [
    {"time": "2024-02-20 15:00:00", "signal": "🔴 SELL @ 1972.80"},
    {"time": "2024-02-20 14:00:00", "signal": "🟢 BUY @ 1968.20"},
]

for s in demo_log:
    st.markdown(f"{s['signal']} | 🕒 *{s['time']}*")

# --- Chart Placeholder ---
st.subheader("Chart Placeholder")
st.image("https://via.placeholder.com/800x400.png?text=TradingView+Chart+Area",
         use_column_width=True)
