from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# the entry point to the Spark structured API
spark = SparkSession.builder.appName("Spark Recap") \
    .master("local[2]") \
    .config("spark.executor.extraClassPath", "spark-sql-kafka-0-10_2.12-3.0.2.jar") \
    .config("spark.driver.extraClassPath", "spark-sql-kafka-0-10_2.12-3.0.2.jar") \
    .config("spark.executor.extraClassPath", "spark-streaming-kafka-0-10_2.12-3.0.2.jar") \
    .config("spark.driver.extraClassPath", "spark-streaming-kafka-0-10_2.12-3.0.2.jar") \
    .getOrCreate()

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "pkc-l6wr6.europe-west2.gcp.confluent.cloud:9092") \
    .option("subscribe", "ufv-demo") \
    .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

if __name__ == "__main__":
    exit(-1)