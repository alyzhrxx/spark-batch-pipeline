# 📊 Praktikum 8 - Real-Time Fraud Detection

## 👨‍💻 Deskripsi
Pada praktikum ini, dilakukan implementasi sistem **real-time fraud detection** menggunakan:
- Apache Kafka (streaming data)
- Apache Spark Streaming (processing data)
- Parquet (penyimpanan data)
- Streamlit (dashboard visualisasi)

---

## ⚙️ Arsitektur
Producer → Kafka → Spark Streaming → Parquet → Dashboard

---

## 📁 File yang Digunakan
- scripts/kafka_producer_bank.py
- scripts/spark_streaming_fraud_v2.py
- dashboard/fraud_dashboard_v2.py

---

## 🚀 Cara Menjalankan

### 1. Jalankan Kafka
```bash
cd kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties