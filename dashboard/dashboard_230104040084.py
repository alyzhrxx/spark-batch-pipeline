import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Smart City Dashboard", layout="wide")

st.title("🚦 Smart City Traffic Monitoring System")

DATA_PATH = "output/traffic"

if not os.path.exists(DATA_PATH):
    st.error("❌ Data belum tersedia. Jalankan Spark dulu.")
else:
    df = pd.read_parquet(DATA_PATH)

    # 🔥 SIDEBAR FILTER
    st.sidebar.header("🔎 Filter Data")

    lokasi_filter = st.sidebar.multiselect(
        "Pilih Lokasi",
        options=df["lokasi"].unique(),
        default=df["lokasi"].unique()
    )

    cuaca_filter = st.sidebar.multiselect(
        "Pilih Cuaca",
        options=df["cuaca"].unique(),
        default=df["cuaca"].unique()
    )

    filtered_df = df[
        (df["lokasi"].isin(lokasi_filter)) &
        (df["cuaca"].isin(cuaca_filter))
    ]

    # 🔥 METRICS
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Data", len(filtered_df))
    col2.metric("Rata-rata Kendaraan", int(filtered_df["jumlah_kendaraan"].mean()))
    col3.metric("Maks Kendaraan", int(filtered_df["jumlah_kendaraan"].max()))

    st.divider()

    # 🔥 TABEL
    st.subheader("📊 Data Traffic")
    st.dataframe(filtered_df, use_container_width=True)

    st.divider()

    # 🔥 GRAFIK UTAMA
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("📈 Trend Kendaraan")
        st.line_chart(filtered_df["jumlah_kendaraan"])

    with col5:
        st.subheader("📊 Distribusi Lokasi")
        lokasi_count = filtered_df["lokasi"].value_counts()
        st.bar_chart(lokasi_count)

    st.divider()

    # 🔥 GRAFIK TAMBAHAN
    st.subheader("🌦️ Pengaruh Cuaca")

    cuaca_group = filtered_df.groupby("cuaca")["jumlah_kendaraan"].mean()
    st.bar_chart(cuaca_group)

    st.divider()

    # 🔥 MACHINE LEARNING
    st.subheader("🤖 Prediksi Traffic (Linear Regression)")

    X = np.arange(len(filtered_df)).reshape(-1, 1)
    y = filtered_df["jumlah_kendaraan"]

    model = LinearRegression()
    model.fit(X, y)

    future_step = st.slider("Prediksi berapa langkah ke depan?", 1, 20, 5)

    future = np.array([[len(filtered_df) + future_step]])
    pred = model.predict(future)

    st.success(f"🚀 Prediksi {future_step} step ke depan: {int(pred[0])} kendaraan")

    st.divider()

    # 🔥 DOWNLOAD DATA
    st.subheader("⬇️ Download Data")

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="traffic_data.csv",
        mime="text/csv"
    )
