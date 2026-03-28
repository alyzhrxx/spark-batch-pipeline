import streamlit as st
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from analytics.transportation_analytics import *
from alerts.transportation_alert import *

st.title("Transportation Decision Dashboard")

DATA_PATH = os.path.join(BASE_DIR, "data/serving/transportation")

def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()

    files = os.listdir(DATA_PATH)
    if not files:
        return pd.DataFrame()

    df_list = []
    for f in files:
        if f.endswith(".parquet"):
            df_list.append(pd.read_parquet(os.path.join(DATA_PATH, f)))

    if df_list:
        return pd.concat(df_list)
    else:
        return pd.DataFrame()

data = load_data()

if data.empty:
    st.warning("No transportation data yet...")
else:
    total_trips, total_revenue, avg_distance = compute_kpis(data)

    st.metric("Total Trips", total_trips)
    st.metric("Total Revenue", total_revenue)
    st.metric("Avg Distance", avg_distance)

    st.subheader("Revenue per City")
    st.bar_chart(revenue_per_city(data))

    st.subheader("Trips per Driver")
    st.bar_chart(trips_per_driver(data))

    st.subheader("Alerts")
    alerts = check_alerts(data)
    for alert in alerts:
        st.error(alert)

    st.subheader("Live Trips")
    st.dataframe(data.tail(20))