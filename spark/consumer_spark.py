from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

# -----------------------------
# Spark Session
# -----------------------------
spark = SparkSession.builder \
    .appName("OrderTracking") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -----------------------------
# Schema Definition
# -----------------------------
order_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("customer", StringType(), True),
    StructField("location", StringType(), True),
    StructField("status", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("price_factor", DoubleType(), True),
    StructField("weather", StringType(), True),
    StructField("delay", IntegerType(), True)
])

# -----------------------------
# Kafka Source Stream
# -----------------------------
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders_topic") \
    .option("startingOffsets", "earliest") \
    .load()

# -----------------------------
# Extract JSON from Kafka value
# -----------------------------
json_df = kafka_df.selectExpr("CAST(value AS STRING) as json_value")

parsed_df = json_df.select(
    from_json(col("json_value"), order_schema).alias("data")
).select("data.*")

# -----------------------------
# Console Sink (Streaming Output)
# -----------------------------
console_query = parsed_df.writeStream \
    .format("console") \
    .option("truncate", False) \
    .outputMode("append") \
    .start()

# -----------------------------
# Keep Stream Running
# -----------------------------
console_query.awaitTermination()