
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

spark = (
    SparkSession.builder
        .appName("DeployMonitoringDemo")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"
        )
        .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = (
    StructType()
        .add("amount", DoubleType())
        .add("currency", StringType())
)

df_raw = (
    spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:29092")
        .option("subscribe", "payments")
        .option("startingOffsets", "earliest")
        .option("failOnDataLoss", "false")
        .load()
)

df_json = df_raw.select(
    from_json(col("value").cast("string"), schema).alias("data")
)

df_clean = df_json.select("data.*")

query = (
    df_clean.writeStream
        .format("console")
        .outputMode("append")
        .option("checkpointLocation", "./checkpoint-deploy-demo")
        .start()
)

query.awaitTermination()
