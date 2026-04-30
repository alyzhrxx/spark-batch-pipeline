from pyspark.sql import SparkSession
import pandas as pd
import random
from datetime import datetime, timedelta
import os

# 🔥 init spark
spark = SparkSession.builder \
    .appName("SmartCityTraffic") \
    .getOrCreate()

# 🔥 buat folder output
os.makedirs("output", exist_ok=True)

# 🔥 generate data dummy
data = []
start_time = datetime.now()

for i in range(100):
    row = {
        "waktu": start_time + timedelta(minutes=i),
        "lokasi": random.choice(["Jakarta", "Bandung", "Surabaya"]),
        "jumlah_kendaraan": random.randint(10, 200),
        "cuaca": random.choice(["Cerah", "Hujan"])
    }
    data.append(row)

# 🔥 ke pandas
pdf = pd.DataFrame(data)

# 🔥 ke spark
df = spark.createDataFrame(pdf)

# 🔥 simpan parquet
df.write.mode("overwrite").parquet("output/traffic")

print("✅ SEMUA DATA BERHASIL DISIMPAN")
