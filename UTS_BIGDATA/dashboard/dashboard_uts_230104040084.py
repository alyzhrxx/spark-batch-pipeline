import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Retail Visitor Dashboard",
    layout="wide"
)

# =====================================
# TITLE
# =====================================

st.title("🛍 Smart Retail Visitor Prediction System")
st.markdown("Dashboard Big Data + Machine Learning")

# =====================================
# PATH
# =====================================

BASE_PATH = "/home/alyzhrxx/bigdata-project/UTS_BIGDATA/output"

# =====================================
# LOAD PARQUET
# =====================================

visitor_total = pd.read_parquet(
    f"{BASE_PATH}/visitor_total"
)

visitor_time = pd.read_parquet(
    f"{BASE_PATH}/visitor_time"
)

ml_df = pd.read_parquet(
    f"{BASE_PATH}/ml_visitor"
)

# =====================================
# SIDEBAR FILTER
# =====================================

st.sidebar.title("🎛 Filter Zone")

zone_filter = st.sidebar.selectbox(
    "Pilih Zone",
    visitor_total["zone"].unique()
)

# =====================================
# FILTER DATA
# =====================================

filtered_total = visitor_total[
    visitor_total["zone"] == zone_filter
]

filtered_time = visitor_time[
    visitor_time["zone"] == zone_filter
]

# =====================================
# KPI
# =====================================

st.subheader("📊 KPI Pengunjung")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Visitor",
        int(filtered_total["total_visitor"].sum())
    )

with col2:
    st.metric(
        "Rata-rata Visitor",
        int(ml_df["visitor_count"].mean())
    )

# =====================================
# FORMAT WINDOW
# =====================================

filtered_time = filtered_time.reset_index(drop=True)

filtered_time["window_time"] = [
    f"{8+i}:00" for i in range(len(filtered_time))
]

# =====================================
# LINE CHART
# =====================================

st.subheader("📈 Grafik Tren Pengunjung")

fig1 = px.line(
    filtered_time,
    x="window_time",
    y="visitor_trend",
    markers=True,
    title=f"Trend Visitor {zone_filter}"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================
# BAR CHART
# =====================================

st.subheader("🏬 Total Pengunjung per Zone")

fig2 = px.bar(
    visitor_total,
    x="zone",
    y="total_visitor",
    color="zone",
    title="Total Visitor Setiap Zone"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================
# MACHINE LEARNING VISUALIZATION
# =====================================

st.subheader("🤖 Prediksi Visitor")

fig3 = px.scatter(
    ml_df,
    x="hour",
    y="visitor_count",
    title="Prediksi Visitor Berdasarkan Jam"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =====================================
# TABLE DATA
# =====================================

st.subheader("📋 Sample Dataset")

st.dataframe(
    ml_df.head(20)
)

# =====================================
# ANALISIS
# =====================================

st.subheader("📝 Analisis")

jam_sibuk = (
    ml_df.groupby("hour")["visitor_count"]
    .mean()
    .idxmax()
)

st.success(
    f"Prediksi jam sibuk pengunjung terjadi sekitar pukul {jam_sibuk}:00"
)

# =====================================
# FOOTER
# =====================================

st.caption("UTS Big Data Technology - Retail Visitor Prediction")