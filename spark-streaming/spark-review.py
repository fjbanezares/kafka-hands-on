from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# the entry point to the Spark structured API
spark = SparkSession.builder.appName("Spark Recap") \
    .master("local[2]") \
    .config("spark.executor.extraClassPath", "spark-sql-kafka-0-10_2.12-3.0.2.jar") \
    .config("spark.driver.extraClassPath", "spark-sql-kafka-0-10_2.12-3.0.2.jar") \
    .getOrCreate()

# read a DF
cars = spark.read.format("json") \
    .option("inferSchema", "true") \
    .load("data/cars")

# select
usefulCarsData = cars.select(
    col("Name"), # column object
    col("Year"), # another column object
    (col("Weight_in_lbs") / 2.2).alias("Weight_in_kg"),
    expr("Weight_in_lbs / 2.2").alias("Weight_in_kg_2")
)

carsWeights = cars.selectExpr("Weight_in_lbs / 2.2")

# filter
europeanCars = cars.filter(col("Origin") != "USA")

# aggregations
averageHP = cars.select(avg(col("Horsepower")).alias("average_hp")) # sum, meam, stddev, min, max

# grouping
countByOrigin = cars.groupBy("Origin").count()

# joining
guitarPlayers = spark.read.option("inferSchema", "true") \
    .json("data/guitarPlayers")

bands = spark.read.option("inferSchema", "true") \
    .json("data/bands")

guitaristsBands = guitarPlayers.join(bands, guitarPlayers["band"] == bands["id"])

# Spark SQL
cars.createOrReplaceTempView("cars")
americanCars = spark.sql("select Name from cars where Origin = 'USA'")

# low-level API: RDDs
sc = spark.sparkContext
numbersRDD = sc.parallelize(range(1, 1000001))

# functional operators
doubles = numbersRDD.map(lambda x: x * 2)

# RDD -> DF
#numbersDF = numbersRDD.toDF(["number"])

# RDD -> DS
numbersDS = spark.createDataset(numbersRDD)

# DS -> RDD
#guitarPlayersRDD = guitarPlayersDS.rdd

# DF -> RDD
carsRDD = cars.rdd

if __name__ == "__main__":
    cars.show()
    cars.printSchema()
