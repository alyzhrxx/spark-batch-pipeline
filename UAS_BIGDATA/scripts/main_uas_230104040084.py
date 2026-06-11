from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from datetime import datetime, timedelta
import random

# =====================================
# SPARK SESSION
# =====================================

spark = SparkSession.builder \
    .appName("SmartHospitalMonitoringSystem") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# =====================================
# GENERATE DATA 120 MENIT
# =====================================

rooms = [
    "ICU",
    "Emergency",
    "Pharmacy",
    "Laboratory"
]

start_time = datetime.now()

data = []

for minute in range(120):

    room = random.choice(rooms)

    patient_count = random.randint(5, 80)

    timestamp = start_time + timedelta(minutes=minute)

    data.append(
        (
            timestamp,
            room,
            patient_count
        )
    )

# =====================================
# DATAFRAME
# =====================================

df = spark.createDataFrame(
    data,
    [
        "timestamp",
        "room",
        "patient_count"
    ]
)

# =====================================
# TOTAL PASIEN PER RUANGAN
# =====================================

room_total = df.groupBy("room").agg(
    sum("patient_count").alias("total_patient")
)

# =====================================
# TREN PASIEN PER 15 MENIT
# =====================================

patient_time = df.groupBy(
    window("timestamp", "15 minutes"),
    "room"
).agg(
    avg("patient_count").alias("patient_trend")
)

# =====================================
# DATASET AI BERBASIS JAM
# =====================================

ml_data = df.withColumn(
    "hour",
    hour("timestamp")
)

ml_hour = ml_data.groupBy(
    "hour"
).agg(
    avg("patient_count").alias("patient_count")
)

# =====================================
# MACHINE LEARNING
# =====================================

assembler = VectorAssembler(
    inputCols=["hour"],
    outputCol="features"
)

ml_ready = assembler.transform(ml_hour)

lr = LinearRegression(
    featuresCol="features",
    labelCol="patient_count"
)

model = lr.fit(ml_ready)

prediction = model.transform(ml_ready)

prediction_output = prediction.select(
    "hour",
    "patient_count",
    "prediction"
)

# =====================================
# SAVE PARQUET
# =====================================

BASE_PATH = "/home/alyzhrxx/bigdata-project/UAS_BIGDATA/output"

room_total.write.mode("overwrite").parquet(
    f"{BASE_PATH}/room_total"
)

patient_time.write.mode("overwrite").parquet(
    f"{BASE_PATH}/patient_time"
)

prediction_output.write.mode("overwrite").parquet(
    f"{BASE_PATH}/ml_patient"
)

print("================================")
print("SMART HOSPITAL MONITORING")
print("================================")
print("✅ room_total saved")
print("✅ patient_time saved")
print("✅ ml_patient saved")
print("================================")

spark.stop()