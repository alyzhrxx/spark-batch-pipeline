from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when
from pyspark.sql.types import StructType, StringType, IntegerType

# 🔥 Spark Session
spark = SparkSession.builder \
    .appName("FraudDetection") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# 🔥 Schema Kafka
schema = StructType() \
    .add("nama", StringType()) \
    .add("rekening", StringType()) \
    .add("jumlah", IntegerType()) \
    .add("lokasi", StringType())

# 🔥 Read dari Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
    .option("subscribe", "bank_topic") \
    .option("startingOffsets", "latest") \
    .load()

# 🔥 Convert ke string
json_df = df.selectExpr("CAST(value AS STRING) as json")

# 🔥 Parse JSON
parsed_df = json_df.select(
    from_json(col("json"), schema).alias("data")
).select("data.*")

# 🔥 Deteksi fraud (lebih jelas pakai when)
fraud_df = parsed_df.withColumn(
    "status",
    when(
        (col("jumlah") > 80000000) | (col("lokasi") == "Luar Negeri"),
        "FRAUD"
    ).otherwise("AMAN")
)

# 🔥 Output ke console
query1 = fraud_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

# 🔥 Simpan ke parquet
query2 = fraud_df.writeStream \
    .format("parquet") \
    .option("path", "stream_data/realtime_output") \
    .option("checkpointLocation", "data/checkpoints") \
    .outputMode("append") \
    .start()

# 🔥 Jalan terus
spark.streams.awaitAnyTermination()
