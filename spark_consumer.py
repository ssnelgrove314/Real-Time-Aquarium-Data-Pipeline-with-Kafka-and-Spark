import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import from_json, col, when, lit, expr
from pyspark.sql.types import TimestampType

# Initialize Spark Session with Kafka and PostgreSQL dependencies
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3,org.postgresql:postgresql:42.5.0") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "aquarium_sensors"

# Define a valid checkpoint directory
CHECKPOINT_DIR = "/tmp/spark_checkpoint"
os.makedirs(CHECKPOINT_DIR, exist_ok=True)  # Ensure the directory exists

# Define Schema for Sensor Data
sensor_schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("sensors", StructType([
        StructField("temperature", FloatType(), True),
        StructField("tds", FloatType(), True),
        StructField("ph", FloatType(), True),
        StructField("nitrate", FloatType(), True),
        StructField("ammonia", FloatType(), True),
        StructField("nitrite", FloatType(), True),
        StructField("gh", FloatType(), True),
        StructField("kh", FloatType(), True),
    ]))
])

# Read data from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

# Extract the JSON value and apply the schema
parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), sensor_schema).alias("data"))

# Schema Validation and Flatten
flattened_df = parsed_df.filter(col("data").isNotNull()).select(
    col("data.timestamp").cast(TimestampType()).alias("timestamp"),  # Cast to TimestampType
    col("data.sensors.temperature").alias("temperature"),
    col("data.sensors.tds").alias("tds"),
    col("data.sensors.ph").alias("ph"),
    col("data.sensors.nitrate").alias("nitrate"),
    col("data.sensors.ammonia").alias("ammonia"),
    col("data.sensors.nitrite").alias("nitrite"),
    col("data.sensors.gh").alias("gh"),
    col("data.sensors.kh").alias("kh")
)

# Add Threshold-Based Derived Columns
thresholds_df = flattened_df.withColumn(
    "temperature_alert", when((col("temperature") < 70) | (col("temperature") > 84), lit("ALERT")).otherwise(lit("NORMAL"))
).withColumn(
    "tds_alert", when((col("tds") < 120) | (col("tds") > 350), lit("ALERT")).otherwise(lit("NORMAL"))
).withColumn(
    "ph_alert", when((col("ph") < 6.0) | (col("ph") > 8.5), lit("ALERT")).otherwise(lit("NORMAL"))
).withColumn(
    "nitrate_alert", when(col("nitrate") > 50, lit("ALERT")).otherwise(lit("NORMAL"))
).withColumn(
    "ammonia_alert", when(col("ammonia") > 0.25, lit("ALERT")).otherwise(lit("NORMAL"))
).withColumn(
    "nitrite_alert", when(col("nitrite") > 0.5, lit("ALERT")).otherwise(lit("NORMAL"))
).withColumn(
    "gh_alert", when((col("gh") < 3) | (col("gh") > 14), lit("ALERT")).otherwise(lit("NORMAL"))
).withColumn(
    "kh_alert", when((col("kh") < 2) | (col("kh") > 12), lit("ALERT")).otherwise(lit("NORMAL"))
)

# Add Monitoring
status_df = thresholds_df.withColumn(
    "overall_status",
    expr("CASE WHEN temperature_alert = 'ALERT' OR tds_alert = 'ALERT' OR ph_alert = 'ALERT' "
         "OR nitrate_alert = 'ALERT' OR ammonia_alert = 'ALERT' OR nitrite_alert = 'ALERT' "
         "OR gh_alert = 'ALERT' OR kh_alert = 'ALERT' THEN 'CRITICAL' ELSE 'NORMAL' END")
)

# PostgreSQL Configuration
POSTGRES_URL = "jdbc:postgresql://localhost:5432/aquarium_data"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "password"

# Write to PostgreSQL using foreachBatch
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", "sensor_readings") \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

query = status_df.writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_postgres) \
    .option("checkpointLocation", CHECKPOINT_DIR) \
    .start()

query.awaitTermination()