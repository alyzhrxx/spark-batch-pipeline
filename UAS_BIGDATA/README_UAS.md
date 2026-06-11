# UAS BIG DATA TECHNOLOGY

## Identitas Mahasiswa

* Nama : Siti Alayda Azzahro
* NIM : 230104040084
* Mata Kuliah : Big Data Technology
* Jenis Ujian : UAS
* Tema : Smart Hospital Monitoring System

---

## Deskripsi Project

Project ini merupakan implementasi pipeline Big Data menggunakan Apache Spark (PySpark), Machine Learning (Linear Regression), Parquet Storage, dan Dashboard Streamlit.

Sistem mensimulasikan data monitoring rumah sakit dengan beberapa ruangan seperti:

* ICU
* Emergency
* Pharmacy
* Laboratory

Data pasien dihasilkan secara acak selama 120 menit dengan jumlah pasien antara 5–80 pasien.

---

## Teknologi yang Digunakan

* Python
* Apache Spark (PySpark)
* Machine Learning (Linear Regression)
* Parquet Storage
* Streamlit
* Plotly

---

## Struktur Project

UAS_BIGDATA/

├── scripts/

│ └── main_uas_230104040084.py

├── dashboard/

│ └── dashboard_230104040084.py

├── output/

│ ├── room_total/

│ ├── patient_time/

│ └── ml_patient/

├── screenshots/

└── README_UAS.md

---

## Proses Big Data Pipeline

### 1. Data Generation

Membangun data simulasi rumah sakit selama 120 menit dengan beberapa ruangan dan jumlah pasien acak.

### 2. Spark Transformation

Melakukan proses:

* Total pasien per ruangan
* Tren pasien per 15 menit
* Dataset AI berbasis jam

### 3. Machine Learning

Menggunakan algoritma Linear Regression untuk melakukan prediksi jumlah pasien berdasarkan jam.

### 4. Parquet Storage

Seluruh hasil transformasi disimpan dalam format Parquet.

### 5. Dashboard Streamlit

Menampilkan:

* KPI Monitoring
* Filter Ruangan
* Grafik Tren Pasien
* Grafik Total Pasien per Ruangan
* Prediksi AI
* Analisis Data

---

## Cara Menjalankan Program

### Jalankan Spark Processing

```bash
python scripts/main_uas_230104040084.py
```

### Jalankan Dashboard

```bash
streamlit run dashboard/dashboard_230104040084.py
```

---

## Output

* File Parquet
* Dashboard Streamlit
* Prediksi Machine Learning
* Analisis Monitoring Rumah Sakit

---

## Kesimpulan

Project berhasil mengimplementasikan pipeline Big Data mulai dari proses data generation, transformasi menggunakan Apache Spark, penyimpanan Parquet, Machine Learning Linear Regression, hingga visualisasi dashboard menggunakan Streamlit.
