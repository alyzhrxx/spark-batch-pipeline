from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder \
    .appName("StreamingTransactions") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = "user_id INT, product STRING, price INT, city STRING, timestamp STRING"

df = spark.readStream \
    .schema(schema) \
    .json("stream_data")

query = df.writeStream \
    .format("parquet") \
    .option("path", "data/serving/stream") \
    .option("checkpointLocation", "logs/checkpoint_stream") \
    .outputMode("append") \
    .start()

query.awaitTermination()
