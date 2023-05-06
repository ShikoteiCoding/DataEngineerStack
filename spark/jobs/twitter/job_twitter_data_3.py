from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import SparkSession, Column

from pyspark.sql.types import TimestampType

import sys
import os


# TODO: access logger from those functions.
def tweet_rank_per_day_per_user() -> Column:
    """compute rank of tweet per day per user"""

    w = Window.partitionBy(F.col("tweet_date"), F.col("user_id")).orderBy(
        F.col("created_ts").asc()
    )

    return F.rank().over(w)


def join_cond_screen_name_over_the_day() -> Column:
    """returns function as condition ot join tweets screen name by user"""

    return (
        (F.col("left.user_id") == F.col("right.user_id"))
        & (F.col("left.tweet_date") == F.col("right.tweet_date"))
        & (F.col("left.screen_name") != F.col("right.screen_name"))
        & (F.col("left.rank_screen_name") == F.col("right.rank_screen_name") - 1)
    )


if __name__ == "__main__":
    # import package
    sys.path.insert(1, os.path.abspath("."))  # Dirty, need to fix it
    from commons.logger import LoggerProvider
    from commons.commons import (
        select_columns,
        read_csv,
        attach_column,
        cast_column,
        join_dataframe,
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
                df,
                [
                    "user_id",
                    "screen_name",
                    "created_at",
                ],
            )

            # create columns
            df = attach_column(df, "tweet_date", parse_date_from_file_name)
            df = cast_column(df, "created_at", TimestampType(), alias="created_ts")
            df = attach_column(df, "rank_screen_name", tweet_rank_per_day_per_user)

            # join dataframe
            df = join_dataframe(
                df.alias("left"),
                df.alias("right"),
                join_cond_screen_name_over_the_day,
                join_type="inner",
            )

            # select dataframe
            df = select_columns(
                df,
                [
                    F.col("left.user_id").alias("user_id"),
                    F.col("left.screen_name").alias("old_screen_name"),
                    F.col("right.screen_name").alias("new_screen_name"),
                    F.col("right.tweet_date").alias("change_date"),
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
