import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Smart Hospital Monitoring",
    layout="wide"
)

# =====================================
# TITLE
# =====================================

st.title("🏥 Smart Hospital Monitoring System")
st.markdown("UAS Big Data Technology")

# =====================================
# LOAD DATA
# =====================================

BASE_PATH = "/home/alyzhrxx/bigdata-project/UAS_BIGDATA/output"

room_total = pd.read_parquet(
    f"{BASE_PATH}/room_total"
)

patient_time = pd.read_parquet(
    f"{BASE_PATH}/patient_time"
)

ml_df = pd.read_parquet(
    f"{BASE_PATH}/ml_patient"
)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("🎛 Filter Room")

selected_room = st.sidebar.selectbox(
    "Pilih Ruangan",
    sorted(room_total["room"].unique())
)

# =====================================
# FILTER
# =====================================

filtered_total = room_total[
    room_total["room"] == selected_room
]

filtered_time = patient_time[
    patient_time["room"] == selected_room
]

# =====================================
# FORMAT WINDOW
# =====================================

filtered_time = filtered_time.reset_index(drop=True)

filtered_time["window_time"] = [
    f"{i*15} Menit"
    for i in range(len(filtered_time))
]

# =====================================
# KPI
# =====================================

st.subheader("📊 KPI Monitoring")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Pasien",
        int(filtered_total["total_patient"].sum())
    )

with col2:
    st.metric(
        "Rata-rata Pasien",
        int(ml_df["patient_count"].mean())
    )

# =====================================
# TREND CHART
# =====================================

st.subheader("📈 Tren Pasien per 15 Menit")

fig1 = px.line(
    filtered_time,
    x="window_time",
    y="patient_trend",
    markers=True,
    title=f"Trend Pasien - {selected_room}"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================
# BAR CHART
# =====================================

st.subheader("🏥 Total Pasien per Ruangan")

fig2 = px.bar(
    room_total,
    x="room",
    y="total_patient",
    color="room"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================
# MACHINE LEARNING
# =====================================

st.subheader("🤖 Prediksi AI")

fig3 = px.scatter(
    ml_df,
    x="hour",
    y="patient_count",
    title="Prediksi Jumlah Pasien Berdasarkan Jam"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =====================================
# TABLE
# =====================================

st.subheader("📋 Dataset AI")

st.dataframe(
    ml_df,
    use_container_width=True
)

# =====================================
# ANALISIS
# =====================================

st.subheader("📝 Analisis")

jam_sibuk = (
    ml_df.groupby("hour")["patient_count"]
    .mean()
    .idxmax()
)

st.success(
    f"Jam dengan rata-rata pasien tertinggi berada pada pukul {jam_sibuk}:00"
)

# =====================================
# FOOTER
# =====================================

st.markdown("---")
st.caption(
    "UAS Big Data Technology - Smart Hospital Monitoring System"
)