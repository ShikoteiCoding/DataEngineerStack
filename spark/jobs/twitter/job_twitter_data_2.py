import os
import time

from pyspark.sql.types import BooleanType, TimestampType
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

    w = Window.partitionBy(
        F.col("reply_date"), F.col("user_id"), F.col("created_at")
    ).orderBy(F.col("created_ts").asc())

    df = (
        df.select(
            "status_id",
            "is_quote",
            "user_id",
            "reply_to_user_id",
            "reply_to_status_id",
            "reply_to_screen_name",
            "created_at",
        )
        .withColumn("is_quote", F.col("is_quote").cast(BooleanType()))
        .withColumn("created_ts", F.col("created_at").cast(TimestampType()))
        .withColumn(
            "reply_date",
            F.regexp_extract(F.input_file_name(), "\\d{4}-\\d{1,2}-\\d{1,2}", 0),
        )
        .withColumn("tweet_number", F.row_number().over(w))
    )

    df_quote = df.filter(F.col("is_quote"))

    df_final = (
        df_quote.alias("quote")
        .join(
            df.alias("all"),
            (F.col("quote.reply_to_status_id") == F.col("all.status_id"))
            & (F.col("quote.created_ts") > F.col("all.created_ts")),
            "left",
        )
        .select(
            F.col("quote.reply_date").alias("reply_date"),
            F.col("quote.user_id").alias("reply_user_id"),
            F.col("all.user_id").alias("original_user_id"),
            F.when(
                F.col("all.created_ts").isNotNull(),
                F.col("quote.created_ts") - F.col("all.created_ts"),
            ).alias("reply_delay"),
            F.col("quote.tweet_number").alias("tweet_number"),
        )
    )

    # Debug
    df_final.printSchema()
    df_final.show(truncate=False, vertical=True)

    # End timer
    end = time.time()
    print(end - start)  # Should go to monitoring endpoints
