from pyspark.sql import functions as F
from pyspark.sql.types import TimestampType
from pyspark.sql.window import Window
from pyspark.sql import SparkSession, Column

import sys
import os


def list_regex_extract_hastags() -> Column:
    """returns function to extract hashtags from text"""

    return F.expr(r"regexp_extract_all(text, '(#\\w+)', 1)")


def last_screen_name_per_day_per_user() -> Column:
    """returns function to create list of screen name ordered by tweet date"""

    w = Window.partitionBy(F.col("tweet_date"), F.col("user_id")).orderBy(
        F.col("created_ts").desc()
    )

    return F.collect_list(F.col("screen_name")).over(w).getItem(0)


def count_source_name_per_day_user() -> Column:
    """returns function to create list of screen name ordered by tweet date"""

    w = Window.partitionBy(F.col("tweet_date"), F.col("user_id"), F.col("source"))

    return F.count(F.col("source")).over(w)


def group_by_fields() -> list[Column]:
    """returns list of columns for group by"""

    return [
        F.col("tweet_date"),
        F.col("user_id"),
        F.col("screen_name"),
    ]


def agg_fields() -> list[Column]:
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
    from commons.logger import LoggerProvider
    from commons.spark_helpers import (
        select_columns,
        read_csv,
        attach_column,
        cast_column,
        group_dataframe,
        parse_date_from_file_name,
    )

    class TestApp(LoggerProvider):
        def __init__(self, app_name: str):
            self.spark = SparkSession.builder.appName(app_name).getOrCreate()
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

            # select columns
            df = select_columns(
                df, ["user_id", "text", "screen_name", "created_at", "source"]
            )

            # creating columns
            df = attach_column(df, "tweet_date", parse_date_from_file_name)
            df = attach_column(df, "hashtags", list_regex_extract_hastags)
            df = cast_column(df, "created_at", TimestampType(), alias="created_ts")
            df = attach_column(
                df, "last_screen_name", last_screen_name_per_day_per_user
            )
            df = attach_column(df, "source_count", count_source_name_per_day_user)

            # group dataframe
            df = group_dataframe(df, group_by_fields(), agg_fields())

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
