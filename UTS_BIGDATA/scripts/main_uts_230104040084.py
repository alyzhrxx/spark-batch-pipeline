from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    hour,
    window,
    col,
    sum as _sum
)
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType
)

from sklearn.linear_model import LinearRegression

import pandas as pd
import random

from datetime import datetime, timedelta

# =====================================
# INIT SPARK
# =====================================

spark = SparkSession.builder \
    .appName("SmartRetailVisitorPrediction") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# =====================================
# ABSOLUTE PATH
# =====================================

BASE_PATH = "/home/alyzhrxx/bigdata-project/UTS_BIGDATA/output"

TOTAL_PATH = f"{BASE_PATH}/visitor_total"
TIME_PATH = f"{BASE_PATH}/visitor_time"
ML_PATH = f"{BASE_PATH}/ml_visitor"

# =====================================
# GENERATE DATA
# =====================================

zones = [
    "FoodCourt",
    "FashionArea",
    "Cinema"
]

data = []

start_time = datetime.now()

for i in range(180):

    row = {
        "timestamp": start_time + timedelta(minutes=i),
        "zone": random.choice(zones),
        "visitor_count": random.randint(10, 500)
    }

    data.append(row)

# =====================================
# SCHEMA
# =====================================

schema = StructType([
    StructField(
        "timestamp",
        TimestampType(),
        True
    ),

    StructField(
        "zone",
        StringType(),
        True
    ),

    StructField(
        "visitor_count",
        IntegerType(),
        True
    )
])

# =====================================
# CREATE DATAFRAME
# =====================================

visitor_df = spark.createDataFrame(
    data,
    schema=schema
)

print("\n=== DATA AWAL ===")

visitor_df.show(10)

# =====================================
# TOTAL VISITOR PER ZONA
# =====================================

visitor_total = visitor_df.groupBy(
    "zone"
).agg(
    _sum("visitor_count").alias("total_visitor")
)

print("\n=== TOTAL VISITOR ===")

visitor_total.show()

# =====================================
# TREN PENGUNJUNG PER 15 MENIT
# =====================================

visitor_time = visitor_df.groupBy(
    window(col("timestamp"), "15 minutes"),
    col("zone")
).agg(
    _sum("visitor_count").alias("visitor_trend")
)

print("\n=== TREN VISITOR ===")

visitor_time.show()

# =====================================
# DATASET MACHINE LEARNING
# =====================================

ml_df = visitor_df.withColumn(
    "hour",
    hour(col("timestamp"))
)

ml_data = ml_df.select(
    "hour",
    "visitor_count"
)

print("\n=== DATA ML ===")

ml_data.show()

# =====================================
# MACHINE LEARNING
# =====================================

pandas_df = ml_data.toPandas()

X = pandas_df[["hour"]]

y = pandas_df["visitor_count"]

model = LinearRegression()

model.fit(X, y)

pandas_df["prediction"] = model.predict(X)

print("\n=== HASIL PREDIKSI ===")

print(pandas_df.head())

# =====================================
# SAVE PARQUET
# =====================================

visitor_total.write.mode(
    "overwrite"
).parquet(TOTAL_PATH)

visitor_time.write.mode(
    "overwrite"
).parquet(TIME_PATH)

spark.createDataFrame(
    pandas_df
).write.mode(
    "overwrite"
).parquet(ML_PATH)

print("\n✅ PARQUET BERHASIL DISIMPAN")

print(TOTAL_PATH)
print(TIME_PATH)
print(ML_PATH)

# =====================================
# VALIDASI PARQUET
# =====================================

print("\n=== VALIDASI PARQUET ===")

spark.read.parquet(
    TOTAL_PATH
).show()

spark.read.parquet(
    TIME_PATH
).show()

spark.read.parquet(
    ML_PATH
).show()

# =====================================
# STOP SPARK
# =====================================

spark.stop()
