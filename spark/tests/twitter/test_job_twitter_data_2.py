"""
Test Twitter Job 2
"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as T

from jobs.twitter.job_twitter_data_2 import (
    parse_date_from_file_name,
    tweet_number_per_day_per_user,
    filter_tweet_being_quotes,
)
from jobs.common import read_csv, attach_column, filter_dataframe, join_dataframe


def test_parse_date_from_file_name(
    spark: SparkSession, transaction_test_df: DataFrame
) -> None:
    """test read of csv date filename to extract"""
    date = "2022-01-01"
    url = f"/tmp/file_{date}.csv"

    # write dataframe with specific filename
    transaction_test_df.write.mode("overwrite").csv(url, header=True)

    # read the temporary stored DataFrame
    df = read_csv(spark, url, header=True, inferSchema=True)

    # apply function
    output = (
        attach_column(df, "input_file_date", parse_date_from_file_name)
        .select("input_file_date")
        .collect()
    )

    expected_output = [
        (date,),
        (date,),
    ]

    assert (
        output == spark.createDataFrame(expected_output, ["input_file_date"]).collect()
    )


def test_tweet_number_per_day_per_user(
    spark: SparkSession, tweet_test_df: DataFrame
) -> None:
    """test compute column of number tweet per day per user"""

    # rename columns to match the transofrmation
    tweet_test_df = tweet_test_df.withColumn("reply_date", F.col("tweet_date"))
    tweet_test_df = tweet_test_df.withColumn("created_ts", F.col("created_at"))

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
