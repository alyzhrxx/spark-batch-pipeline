from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, DoubleType
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("TransportationStreaming") \
    .getOrCreate()

schema = StructType() \
    .add("trip_id", StringType()) \
    .add("driver_id", StringType()) \
    .add("passenger_id", StringType()) \
    .add("city", StringType()) \
    .add("distance_km", DoubleType()) \
    .add("fare", DoubleType()) \
    .add("timestamp", StringType())

df = spark.readStream \
    .schema(schema) \
    .json("stream_data/transportation")

query = df.writeStream \
    .format("parquet") \
    .option("path", "data/serving/transportation") \
    .option("checkpointLocation", "data/checkpoint/transportation") \
    .outputMode("append") \
    .start()

query.awaitTermination()