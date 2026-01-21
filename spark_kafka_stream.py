

print(">>> RUNNING spark_kafka_stream.py")

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType

# ---------------------------------------
# 1. Create SparkSession (MATCHES Spark 3.5.0)
# ---------------------------------------
spark = (
    SparkSession.builder
        .appName("KafkaStreamDemo")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"
        )
        .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# ---------------------------------------
# 2. Read from Kafka Topic "payments"
# ---------------------------------------
df_raw = (
    spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:29092")
        .option("subscribe", "payments")
        .option("startingOffsets", "latest")
        .option("failOnDataLoss", "false")
        .load()
)

# Kafka value is bytes → convert to string
df_strings = df_raw.selectExpr("CAST(value AS STRING) as json_value")

# ---------------------------------------
# 3. Define Schema for JSON messages
# ---------------------------------------
schema = (
    StructType()
        .add("amount", DoubleType())
        .add("currency", StringType())
)

df_parsed = (
    df_strings
        .select(from_json(col("json_value"), schema).alias("data"))
        .select("data.*")
)

# Example transformation
df_parsed = df_parsed.withColumn("amount_usd", col("amount") * 1.1)

# ---------------------------------------
# 4. Write output to console in real-time
# ---------------------------------------
query = (
    df_parsed.writeStream
        .outputMode("append")
        .format("console")
        .option("truncate", False)
        .option("checkpointLocation", "./checkpoint-sim")
        .start()
)

query.awaitTermination()

# import json
# import time
# import random
# from kafka import KafkaProducer
#
# print(">>> STARTING payments producer")
#
# producer = KafkaProducer(
#     bootstrap_servers="localhost:29092",   # external Kafka port
#     value_serializer=lambda v: json.dumps(v).encode("utf-8"),
# )
#
# currencies = ["USD", "EUR", "CAD", "GBP", "BRL"]
# amounts = [50, 75, 100, 150, 200, 250]
#
# try:
#     while True:
#         message = {
#             "amount": random.choice(amounts),
#             "currency": random.choice(currencies),
#         }
#
#         producer.send("payments", value=message)
#         producer.flush()
#
#         print("Produced:", message)
#
#         time.sleep(2)  # produce every 2 seconds
#
# except KeyboardInterrupt:
#     print("\nStopping producer...")
#
# finally:
#     producer.close()
