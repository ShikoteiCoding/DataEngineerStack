from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import SparkSession

from pyspark.sql.types import TimestampType, BooleanType

from typing import Callable

import sys
import os


# TODO: Access logger from those functions.
def tweet_number_per_day_per_user() -> Callable:
    """returns function to count number of tweet per day per user"""

    w = Window.partitionBy(F.col("reply_date"), F.col("user_id")).orderBy(
        F.col("created_ts").asc()
    )

    return F.row_number().over(w)


def filter_tweet_being_quotes() -> Callable:
    """returns function as condition to filter quote tweets"""

    return F.col("is_quote")


def join_cond_tweets_by_status() -> Callable:
    """returns function as condition to join tweet dataframes by status"""
    return (F.col("quote.reply_to_status_id") == F.col("all.status_id")) & (
        F.col("quote.created_ts") > F.col("all.created_ts")
    )


def compute_tweet_delay() -> Callable:
    """returns function to select timestamp and compute the diff from original tweet"""

    return F.when(
        F.col("all.created_ts").isNotNull(),
        F.col("quote.created_ts") - F.col("all.created_ts"),
    ).alias("reply_delay")


if __name__ == "__main__":
    # Import package
    sys.path.insert(1, os.path.abspath("."))  # Dirty, need to fix it
    from jobs.spark_logger import LoggerProvider
    from jobs.common import (
        select_columns,
        read_csv,
        attach_column,
        cast_column,
        filter_dataframe,
        join_dataframe,
        parse_date_from_file_name,
    )

    class TestApp(LoggerProvider):
        def __init__(self, app_name: str):
            self.spark = SparkSession.builder.appName(app_name or None).getOrCreate()
            self.logger = self.get_logger(self.spark)

        def run(self):
            # read the file
            self.logger.info("Reading the file")
            df = read_csv(
                self.spark,
                "/data",
                header=True,
                sep=",",
                quote='"',
                escape='"',
                multiLine=True,
            )

            # select
            df = select_columns(
                df,
                [
                    "status_id",
                    "is_quote",
                    "user_id",
                    "reply_to_user_id",
                    "reply_to_status_id",
                    "reply_to_screen_name",
                    "created_at",
                ],
            )

            # create columns
            df = cast_column(df, "is_quote", BooleanType())
            df = cast_column(df, "created_at", TimestampType(), alias="created_ts")
            df = attach_column(df, "reply_date", parse_date_from_file_name)
            df = attach_column(df, "tweet_number", tweet_number_per_day_per_user)

            # filter dataframe
            df_quote = filter_dataframe(df, filter_tweet_being_quotes)

            # join dataframe
            df = join_dataframe(
                df_quote.alias("quote"),
                df.alias("df"),
                join_cond_tweets_by_status,
                join_type="inner",
            )

            # select dataframe
            df = select_columns(
                df,
                [
                    F.col("quote.reply_date").alias("reply_date"),
                    F.col("quote.user_id").alias("reply_user_id"),
                    F.col("all.user_id").alias("original_user_id"),
                    compute_tweet_delay(),
                    F.col("quote.tweet_number").alias("tweet_number"),
                ],
            )

            # print schema
            df.printSchema()
            df.show(truncate=False, vertical=True)

        def launch(self):
            self.logger.info("Launching the application")

        def stop(self):
            self.spark.stop()

    app = TestApp(app_name="test_app")

    app.launch()

    app.run()

    app.stop()
