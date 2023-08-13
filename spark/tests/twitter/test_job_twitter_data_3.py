"""
Test Twitter Job 3
"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as T

from spark_etls.twitter_jobs.job_twitter_data_3 import (
    tweet_rank_per_day_per_user,
    join_cond_screen_name_over_the_day,
)
from commons.spark_helpers import attach_column, join_dataframe


def test_tweet_rank_per_day_per_user(
    spark: SparkSession, tweet_test_df: DataFrame
) -> None:
    """test compute rank or tweet per day per user"""

    output = (
        attach_column(tweet_test_df, "rank_screen_name", tweet_rank_per_day_per_user)
        .select("rank_screen_name")
        .collect()
    )

    expected_output = [
        (1,),
        (1,),
        (2,),
        (1,),
        (2,),
        (1,),
        (2,),
        (3,),
        (1,),
    ]

    assert (
        output == spark.createDataFrame(expected_output, ["rank_screen_name"]).collect()
    )


def test_join_cond_screen_name_over_the_day(
    spark: SparkSession, tweet_test_df: DataFrame
) -> None:
    """test join condition to differentiate screen name change"""
    columns = [
        "left.user_id",
        "left.screen_name",
        "right.screen_name",
        "right.tweet_date",
    ]

    output = attach_column(
        tweet_test_df, "rank_screen_name", tweet_rank_per_day_per_user
    )

    # join dataframe
    output = (
        join_dataframe(
            output.alias("left"),
            output.alias("right"),
            join_cond_screen_name_over_the_day,
            join_type="inner",
        )
        .select(columns)
        .collect()
    )

    expected_output = [
        (1, "Alice", "Alice2", "2022-01-01"),
        (2, "Charlie", "Charlie2", "2022-01-01"),
        (3, "David", "David2", "2022-01-01"),
        (3, "David2", "David3", "2022-01-01"),
    ]

    assert output == spark.createDataFrame(expected_output, columns).collect()
