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
    # KPI
    total_trips, total_revenue, avg_distance = compute_kpis(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trips", total_trips)
    col2.metric("Total Revenue", int(total_revenue))
    col3.metric("Avg Distance", round(avg_distance, 2))

    # Alerts
    st.subheader("Traffic Alerts")
    alerts = check_alerts(data)
    for alert in alerts:
        st.error(alert)

    # Bar Charts
    st.subheader("Fare per City")
    st.bar_chart(revenue_per_city(data))

    st.subheader("Vehicle Distribution")
    vd = vehicle_distribution(data)
    if vd is not None:
        st.bar_chart(vd)

    # Line Charts
    st.subheader("Real-Time Traffic")
    rt = realtime_trips(data)
    if rt is not None:
        st.line_chart(rt)

    st.subheader("Mobility Trend")
    mt = mobility_trend(data)
    if mt is not None:
        st.line_chart(mt)

    # Tables
    st.subheader("Abnormal Trips")
    st.dataframe(abnormal_trips(data))

    st.subheader("Live Trips")
    st.dataframe(data.tail(20))