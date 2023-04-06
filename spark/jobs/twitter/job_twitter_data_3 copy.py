import os
import time

from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pyspark.sql import SparkSession

if __name__ == "__main__":
    print("Compute is starting...")
    app_name = "ComputeSpark1"
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    # Start timer
    start = time.time()

    # Read Dataset
    print("Reading dataset")
    # Demo read.
    url = "/data"
    df = spark.read.csv(
        url, header=True, sep=",", quote='"', escape='"', multiLine=True
    )

    # Partition
    w = Window.partitionBy(F.col("tweet_date"), F.col("user_id")).orderBy(
        F.col("created_ts").asc()
    )

    base_df = (
        df.select(
            F.col("user_id"),
            F.col("screen_name"),
            F.col("created_at"),
        )
        .withColumn(
            "tweet_date",
            F.regexp_extract(F.input_file_name(), "\\d{4}-\\d{1,2}-\\d{1,2}", 0),
        )
        .withColumn("created_ts", F.col("created_at").cast(TimestampType()))
        .withColumn("rank_name", F.rank().over(w))
    )

    cond = [
        (F.col("left.user_id") == F.col("right.user_id"))
        & (F.col("left.tweet_date") == F.col("right.tweet_date"))
        & (F.col("left.screen_name") != F.col("right.screen_name"))
        & (F.col("left.rank_name") == F.col("right.rank_name") - 1)
    ]

    df = (
        base_df.alias("left")
        .join(base_df.alias("right"), cond, "inner")
        .select(
            F.col("left.user_id").alias("user_id"),
            F.col("left.screen_name").alias("old_screen_name"),
            F.col("right.screen_name").alias("new_screen_name"),
            F.col("right.tweet_date").alias("change_date"),
        )
    )

    # Debug
    df.printSchema()
    df.show(truncate=False, vertical=True)

    # End timer
    end = time.time()
    print(end - start)  # Should go to monitoring endpoints
