from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
from pyspark.sql import SparkSession, DataFrame

from typing import Callable

import sys
import os


# TODO: Access logger from those functions.
def parse_date_from_file_name() -> Callable:
    """returns function to parse date from file name"""

    return F.regexp_extract(F.input_file_name(), "\\d{4}-\\d{1,2}-\\d{1,2}", 0)


def list_regex_extract_hastags() -> Callable:
    """returns function to extract hashtags from text"""

    return F.expr(r"regexp_extract_all(text, '(#\\w+)', 1)")


def last_screen_name_per_day_per_user() -> Callable:
    """returns function to create list of screen name ordered by tweet date"""

    w = Window.partitionBy(F.col("tweet_date"), F.col("user_id")).orderBy(
        F.col("created_at").desc()
    )

    return F.collect_list(F.col("screen_name")).over(w).getItem(0)


def count_source_name_per_day_user() -> Callable:
    """returns function to create list of screen name ordered by tweet date"""

    w = Window.partitionBy(F.col("tweet_date"), F.col("user_id"), F.col("source"))

    return F.count(F.col("source")).over(w)


def group_by_fields() -> list[Callable]:
    """returns list of columns for group by"""

    return [
        F.col("tweet_date"),
        F.col("user_id"),
        F.col("screen_name"),
    ]


def agg_fields() -> list[Callable]:
    """returns list of columns for aggregate functions"""

    return [
        F.count(F.col("user_id")).alias("num_tweets"),
        F.map_from_entries(
            F.array_distinct(
                F.arrays_zip(
                    F.collect_list("source"),
                    F.collect_list("source_count"),
                )
            )
        ).alias("tweet_sources"),
        F.array_distinct(F.flatten(F.collect_set(F.col("hashtags")))).alias("hashtags"),
    ]


if __name__ == "__main__":
    # Import package
    sys.path.insert(1, os.path.abspath("."))  # Dirty, need to fix it
    from jobs.spark_logger import LoggerProvider
    from jobs.common import (
        select_columns,
        read_csv,
        attach_column,
        cast_column,
        group_dataframe,
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

            # Select
            df = select_columns(
                df, ["user_id", "text", "screen_name", "created_at", "source"]
            )

            # Creating columns
            df = attach_column(df, "tweet_date", parse_date_from_file_name)
            df = attach_column(df, "hashtags", list_regex_extract_hastags)
            df = cast_column(df, "created_at", TimestampType())
            df = attach_column(
                df, "last_screen_name", last_screen_name_per_day_per_user
            )
            df = attach_column(df, "source_count", count_source_name_per_day_user)

            df = group_dataframe(df, group_by_fields, agg_fields)

            # Print schema
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
