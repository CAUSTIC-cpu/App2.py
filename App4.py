import pandas as pd
import streamlit as st  # Changed from pandas to streamlit

# --- Streamlit Config ---
st.set_page_config(page_title="XAUUSD Fibonacci Demo", layout="wide")
st.title("GOLD (XAU/USD) Fibonacci Signal Scanner (Demo)")

# --- Static Data Generation ---
@st.cache_data
def get_static_data():
    # Generate dummy data for 100 periods
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
high = df["High"].max()  # Will be 1950 + 99*0.5 + 2.5 = 2001.0
low = df["Low"].min()    # Will be 1950 - 2.0 = 1948.0

levels = {
    "0.0%": high,
    "23.6%": high - (high - low) * 0.236,
    "38.2%": high - (high - low) * 0.382,
    "50.0%": high - (high - low) * 0.5,
    "61.8%": high - (high - low) * 0.618,
    "78.6%": high - (high - low) * 0.786,
    "100.0%": low,
}

# --- Display Fibonacci Levels ---
st.subheader("Fibonacci Levels (Demo Data)")
fib_df = pd.DataFrame(levels.items(), columns=["Level", "Price"])
st.dataframe(fib_df.set_index("Level").style.format({"Price": "{:.2f}"}))

# --- Static Signal Values ---
latest_price = 1975.50  # Between 38.2% and 61.8% levels
current_volume = 145000
timestamp = df["Time"].iloc[-1].strftime("%Y-%m-%d %H:%M:%S")

# --- Fixed Signal for Testing ---
st.subheader("Demo Signal")
st.metric(label="Current Price", value=f"${latest_price:.2f}")
st.markdown("**Signal:** 🔴 **SELL** @ 1975.50")
st.markdown("**Risk/Reward:** Risk/Reward: 2.2x (60%)")

# --- Static Signal Log ---
st.subheader("Signal Log (Demo)")
demo_log = [
    {"time": "2024-02-20 15:00:00", "signal": "🔴 SELL @ 1972.80"},
    {"time": "2024-02-20 14:00:00", "signal": "🟢 BUY @ 1968.20"},
    {"time": "2024-02-20 13:00:00", "signal": "⚪ No strong signal"},
]

for s in demo_log:
    st.markdown(f"{s['signal']} | 🕒 *{s['time']}*")

# --- Chart Placeholder ---
st.subheader("Chart Placeholder")
st.image("https://via.placeholder.com/800x400.png?text=TradingView+Chart+Area", 
         use_column_width=True)

# --- Disabled Auto Refresh ---
st.subheader("Auto Refresh (Disabled in Demo)")
st.write("Refresh functionality disabled for static demo")
