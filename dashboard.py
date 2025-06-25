import streamlit as st
from datetime import date, timedelta
from data_fetcher import get_commodity_data
from predictor import train_model, predict_next_close
from alert import should_alert

# ─────────────────────────────────────────────────────────────────────────────
# ✅ All Core Commodities
# ─────────────────────────────────────────────────────────────────────────────
commodities = {
    # Precious & Industrial Metals
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Copper": "HG=F",
    "Platinum": "PL=F",
    "Palladium": "PA=F",

    # Energy
    "Crude Oil WTI": "CL=F",
    "Crude Oil Brent": "BZ=F",
    "Natural Gas": "NG=F",
    "Gasoline": "RB=F",
    "Heating Oil": "HO=F",

    # Grains
    "Corn": "ZC=F",
    "Wheat": "ZW=F",
    "Soybeans": "ZS=F",
    "Oats": "ZO=F",
    "Rough Rice": "ZR=F",

    # Softs
    "Coffee": "KC=F",
    "Cocoa": "CC=F",
    "Sugar": "SB=F",
    "Cotton": "CT=F",
    "Orange Juice": "OJ=F",

    # Livestock
    "Live Cattle": "LE=F",
    "Feeder Cattle": "GF=F",
    "Lean Hogs": "HE=F",
}

# ─────────────────────────────────────────────────────────────────────────────
# 🔧 Page Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Commodity Predictor", layout="wide")

st.title("🧠 AI Commodity Price Predictor")
st.subheader("Select a Commodity")

# ─────────────────────────────────────────────────────────────────────────────
# 🎛️ Buttons for Commodities (Row of 4 per line)
# ─────────────────────────────────────────────────────────────────────────────
cols_per_row = 4
commodity_items = list(commodities.items())

for i in range(0, len(commodity_items), cols_per_row):
    row = st.columns(cols_per_row)
    for j in range(cols_per_row):
        if i + j < len(commodity_items):
            label, symbol = commodity_items[i + j]
            if row[j].button(label):
                st.session_state["selected_ticker"] = symbol
                st.session_state["selected_label"] = label

# Default to Gold
ticker = st.session_state.get("selected_ticker", "GC=F")
label = st.session_state.get("selected_label", "Gold")
st.markdown(f"### 📊 **Currently viewing:** `{label}` (`{ticker}`)")

# ─────────────────────────────────────────────────────────────────────────────
# 📈 Data + Model Prediction + Alert Logic
# ─────────────────────────────────────────────────────────────────────────────
end = date.today()
start = end - timedelta(days=180)

df = get_commodity_data(ticker, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

if df is not None and not df.empty:
    model, feature_df = train_model(df)
    predicted = predict_next_close(model, feature_df)
    current = float(feature_df["Close"].iloc[-1].item())
    alert, signal, change = should_alert(current, predicted)

    k1, k2, k3 = st.columns(3)
    k1.metric("📈 Current Price", f"${current:,.2f}")
    k2.metric("🤖 Predicted Close", f"${predicted:,.2f}")
    k3.metric("📊 Expected Change", f"{change:.2f}%")

    if alert:
        st.success(f"🚨 {signal} SIGNAL TRIGGERED — expected change {change:.2f}%")
    else:
        st.info("✅ No actionable signal right now.")

    st.divider()
else:
    st.warning("⚠️ No data found or failed to load. Try another commodity.")
