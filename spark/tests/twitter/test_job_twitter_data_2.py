"""
Test Twitter Job 2
"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as T

from spark_etls.twitter_jobs.job_twitter_data_2 import (
    tweet_number_per_day_per_user,
    filter_tweet_being_quotes,
)
from commons.spark_helpers import (
    attach_column,
    filter_dataframe,
)


def test_tweet_number_per_day_per_user(
    spark: SparkSession, tweet_test_df: DataFrame
) -> None:
    """test compute column of number tweet per day per user"""

    # rename columns to match the transformation
    tweet_test_df = tweet_test_df.withColumn("reply_date", F.col("tweet_date"))

    output = (
        attach_column(tweet_test_df, "tweet_number", tweet_number_per_day_per_user)
        .select("tweet_number")
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

    assert output == spark.createDataFrame(expected_output, ["tweet_number"]).collect()


def test_filter_tweet_being_quotes(
    spark: SparkSession, tweet_quote_test_df: DataFrame
) -> None:
    """test filter of tweets being quotes"""

    output = (
        filter_dataframe(tweet_quote_test_df, filter_tweet_being_quotes)
        .select("is_quote")
        .collect()
    )

    expected_output = [
        (True,),
        (True,),
    ]

    assert output == spark.createDataFrame(expected_output, ["is_quote"]).collect()


# TODO: test join, yet not fully understood dataset
