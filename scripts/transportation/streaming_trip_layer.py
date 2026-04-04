from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("TransportationStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Schema HARUS sesuai generator
schema = StructType() \
    .add("trip_id", IntegerType()) \
    .add("driver_id", StringType()) \
    .add("passenger_id", StringType()) \
    .add("city", StringType()) \
    .add("distance_km", DoubleType()) \
    .add("fare", DoubleType()) \
    .add("vehicle_type", StringType()) \
    .add("timestamp", StringType())

# Read streaming JSON
df = spark.readStream \
    .schema(schema) \
    .json("stream_data/transportation")

# Convert timestamp (penting untuk chart)
df = df.withColumn("timestamp", to_timestamp("timestamp"))

# Write ke parquet
query = df.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("path", "data/serving/transportation") \
    .option("checkpointLocation", "data/checkpoint/transportation") \
    .start()

query.awaitTermination()