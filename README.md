# Spark Batch & Streaming Data Pipeline

## Overview

This project implements a **Big Data pipeline** using **Apache Spark** for both batch and streaming data processing.
The system simulates real-time e-commerce transactions, processes them using Spark Structured Streaming, and visualizes results through a Streamlit dashboard.

The pipeline consists of:

* Transaction generator (simulated real-time data)
* Spark streaming processing
* Batch data pipeline
* Real-time analytics dashboard

---

## Project Architecture

Transaction Generator → Spark Streaming → Data Storage → Analytics Layer → Dashboard

1. **Transaction Generator**

   * Generates random e-commerce transactions in JSON format.
   * Stored in `stream_data/`.

2. **Streaming Layer**

   * Apache Spark Structured Streaming processes incoming transaction data.
   * Aggregations and transformations are performed in real-time.

3. **Batch Processing**

   * Batch pipeline processes historical data.
   * Outputs curated datasets for analytics.

4. **Serving Layer**

   * Processed data stored in:

   ```
   data/serving/
   ```

5. **Dashboard**

   * Built using **Streamlit**
   * Displays real-time analytics.

---

## Project Structure

```
spark-batch-pipeline
│
├── dashboard
│   └── dashboard_streamlit.py
│
├── data
│   ├── raw
│   ├── clean
│   ├── curated
│   └── serving
│
├── logs
│
├── scripts
│   ├── transaction_generator.py
│   ├── streaming_layer.py
│   ├── analytics_layer.py
│   └── batch_pipeline_enterprise.py
│
├── stream_data
│
└── .gitignore
```

---

## Technologies Used

* Python
* Apache Spark
* Spark Structured Streaming
* Pandas
* Streamlit
* Git & GitHub

---

## Running the Project

### 1. Activate virtual environment

```
source venv/bin/activate
```

### 2. Run transaction generator

```
python scripts/transaction_generator.py
```

### 3. Run Spark streaming

```
spark-submit scripts/streaming_layer.py
```

### 4. Run dashboard

```
python -m streamlit run dashboard/dashboard_streamlit.py
```

---

## Dashboard Features

The real-time dashboard includes:

* Total transactions (KPI metrics)
* Revenue per city
* Top products
* Revenue trend
* Live transaction table

---

## Output Example

Streaming results are stored in:

```
data/serving/stream
```

Output format: **Parquet files**

---

## Author

**Name:** Alyzhrxx (Siti Alayda Azzahro)
**Project:** Big Data Spark Pipeline
