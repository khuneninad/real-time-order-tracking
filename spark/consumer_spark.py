from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

spark = SparkSession.builder.appName("OrderTracking").getOrCreate()

schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("location", StringType()),
    StructField("status", StringType()),
    StructField("timestamp", StringType()),
    StructField("price_factor", DoubleType()),
    StructField("weather", StringType()),
    StructField("delay", IntegerType())
])

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "order_tracking") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)")

parsed_df = json_df.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

query = parsed_df.writeStream \
    .format("console") \
    .start()

query.awaitTermination()