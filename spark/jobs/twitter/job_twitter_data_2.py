from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import SparkSession

from pyspark.sql.types import TimestampType, BooleanType

from typing import Callable

import sys
import os


# TODO: Access logger from those functions.
def parse_date_from_file_name() -> Callable:
    """returns function to parse date from file name"""

    return F.regexp_extract(F.input_file_name(), "\\d{4}-\\d{1,2}-\\d{1,2}", 0)


def tweet_number_per_day_per_user() -> Callable:
    """returns function to count number of tweet per day per user"""

    w = Window.partitionBy(
        F.col("reply_date"), F.col("user_id"), F.col("created_at")
    ).orderBy(F.col("created_ts").asc())

    return F.row_number().over(w)


def filter_tweet_being_quotes() -> Callable:
    """returns function as condition to filter quote tweets"""
    return F.col("is_quote")


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
        filter_dataframe,
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

            # creating columns
            df = cast_column(df, "is_quote", BooleanType())
            df = cast_column(df, "created_ts", TimestampType(), alias="created_at")
            df = attach_column(df, "reply_date", parse_date_from_file_name)
            df = attach_column(df, "tweet_number", tweet_number_per_day_per_user)

            # filter dataframe
            df = filter_dataframe(df, filter_tweet_being_quotes)

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
