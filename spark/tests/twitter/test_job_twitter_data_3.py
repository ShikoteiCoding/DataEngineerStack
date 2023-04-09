"""
Test Twitter Job 3
"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as T

from jobs.twitter.job_twitter_data_3 import tweet_rank_per_day_per_user
from jobs.common import cast_column, attach_column


def test_tweet_rank_per_day_per_user(spark: SparkSession, tweet_test_df: DataFrame):
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

    assert output == spark.createDataFrame(expected_output, ["rank_screen_name"]).collect()