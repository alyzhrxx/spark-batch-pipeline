import streamlit as st
import pandas as pd
import os

st.title("Real-Time Transaction Dashboard")

# Path ke folder data streaming
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data/serving/stream")

# Function load data parquet
def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()

    files = os.listdir(DATA_PATH)
    if not files:
        return pd.DataFrame()

    df_list = []
    for f in files:
        if f.endswith(".parquet"):
            file_path = os.path.join(DATA_PATH, f)
            df = pd.read_parquet(file_path)
            df_list.append(df)

    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        return pd.DataFrame()


data = load_data()

if data.empty:
    st.warning("No streaming data yet...")
else:

    # =========================
    # KPI METRICS
    # =========================
    st.subheader("Total Transactions")
    st.metric("Transactions", len(data))

    # =========================
    # REVENUE PER CITY
    # =========================
    st.subheader("Revenue per City")
    city_rev = data.groupby("city")["price"].sum()
    st.bar_chart(city_rev)

    # =========================
    # TOP PRODUCTS
    # =========================
    st.subheader("Top Products")
    prod = data.groupby("product")["price"].sum()
    st.bar_chart(prod)

    # =========================
    # REVENUE TREND
    # =========================
    st.subheader("Revenue Trend")

    data["timestamp"] = pd.to_datetime(data["timestamp"])
    trend = data.groupby(data["timestamp"].dt.floor("T"))["price"].sum()

    st.line_chart(trend)

    # =========================
    # LIVE TRANSACTION TABLE
    # =========================
    st.subheader("Live Transactions")
    st.dataframe(data.tail(20))