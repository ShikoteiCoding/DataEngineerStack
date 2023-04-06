"""
Test Twitter Job 1
"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as T

from jobs.twitter.job_twitter_data_1 import (
    list_regex_extract_hastags,
    last_screen_name_per_day_per_user,
    count_source_name_per_day_user,
    group_by_fields,
    agg_fields,
)
from jobs.common import attach_column, group_dataframe


def test_list_regex_extract_hastags(spark: SparkSession, tweet_test_df: DataFrame):
    """test extraction of multiple hastags in text column"""

    # apply the function to the DataFrame
    output = (
        attach_column(tweet_test_df, "hashtags", list_regex_extract_hastags)
        .select("hashtags")
        .collect()
    )

    expected_output = [
        (["#Tweets", "#awesome"],),
        (["#Hashtags", "#awesome"],),
        (["#test"],),
        (["#pyspark"],),
        (["#DataEngineer"],),
        ([],),
        ([],),
        ([],),
        ([],),
    ]
    assert output == spark.createDataFrame(expected_output, ["hashtags"]).collect()


def test_last_screen_name_per_day_per_user(
    spark: SparkSession, tweet_test_df: DataFrame
):
    """test subgroup last screen name per fields"""
    # apply the function to the DataFrame
    output = (
        attach_column(
            tweet_test_df, "list_screen_name", last_screen_name_per_day_per_user
        )
        .select("list_screen_name")
        .collect()
    )

    # Check if the output is as expected
    expected_output = [
        ("Bob",),
        ("Alice2",),
        ("Alice2",),
        ("Charlie2",),
        ("Charlie2",),
        ("David3",),
        ("David3",),
        ("David3",),
        ("David",),
    ]
    assert (
        output == spark.createDataFrame(expected_output, ["list_screen_name"]).collect()
    )


def test_count_source_name_per_user(spark: SparkSession, tweet_test_df: DataFrame):
    """test subgroup count per key per fields"""
    columns = ["user_id", "source", "source_name_count"]

    # apply the function to the DataFrame
    # force deternimistic ordering - testing only
    output = (
        attach_column(
            tweet_test_df, "source_name_count", count_source_name_per_day_user
        )
        .sort(F.col("user_id"), F.col("created_at").asc())
        .select(columns)
        .collect()
    )

    expected_output = [
        (0, "Android", 1),
        (1, "Android", 1),
        (1, "iPhone", 1),
        (2, "Android", 2),
        (2, "Android", 2),
        (3, "iPhone", 1),
        (3, "Android", 2),
        (3, "Android", 2),
        (3, "Web", 1),
    ]

    assert output == spark.createDataFrame(expected_output, columns).collect()


def test_group_and_agg(spark: SparkSession, tweet_pre_agg_test_df: DataFrame):
    """test group and aggregation"""

    columns = [
        "tweet_date",
        "user_id",
        "screen_name",
        "num_tweets",
        "tweet_sources",
        "hashtags",
    ]

    # apply the group_fields function to the DataFrame
    # force deternimistic ordering - testing only
    output = (
        group_dataframe(tweet_pre_agg_test_df, group_by_fields, agg_fields)
        .sort(F.col("user_id"), F.col("tweet_date").asc())
        .select(columns)
        .select(F.array_sort("hashtags").alias("hashtags"))
        .collect()
    )

    expected_output = [
        ("2022-01-01", 0, "Bob", 1, {"Android": 1}, []),
        ("2022-01-01", 1, "Alice2", 2, {"iPhone": 1, "Android": 1}, ["#awesome"]),
        ("2022-01-01", 2, "Charlie2", 2, {"Android": 2}, ["#twitter", "#awesome"]),
        (
            "2022-01-01",
            3,
            "David3",
            3,
            {"iPhone": 1, "Android": 2},
            ["#awesome", "#twitter"],
        ),
        ("2022-01-02", 3, "David", 1, {"Web": 1}, ["#twitter"]),
    ]

    assert (
        output
        == spark.createDataFrame(expected_output, columns)
        .select(F.array_sort("hashtags").alias("hashtags"))
        .collect()
    )
