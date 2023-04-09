import findspark

findspark.init()

import pytest

from pyspark.sql import SparkSession, DataFrame


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    spark = (
        SparkSession.builder.master("local[1]")
        .appName("local-tests")
        .config("spark.executor.cores", "1")
        .config("spark.executor.instances", "1")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .getOrCreate()
    )
    yield spark
    spark.stop()


@pytest.fixture(scope="session")
def transaction_test_df(spark: SparkSession) -> DataFrame:
    df = spark.createDataFrame(
        data=[
            (0, 1000.00, "first transaction"),
            (1, 3000.00, "second transaction"),
        ],
        schema=["transaction_id", "amount", "description"],
    )
    return df


@pytest.fixture(scope="session")
def people_test_df(spark: SparkSession) -> DataFrame:
    df = spark.createDataFrame(
        data=[
            ("Alice", 25, "F"),
            ("Bob", 30, "M"),
            ("Charlie", 35, "M"),
            ("David", 35, "M"),
        ],
        schema=["name", "age", "gender"],
    )
    return df


@pytest.fixture(scope="session")
def tweet_test_df(spark: SparkSession) -> DataFrame:
    df = spark.createDataFrame(
        data=[
            (
                "Bob",
                0,
                "F",
                "2022-01-01 12:00:00",
                "2022-01-01",
                "Android",
                "#Tweets are #awesome",
            ),
            (
                "Alice",
                1,
                "F",
                "2022-01-01 12:00:00",
                "2022-01-01",
                "Android",
                "#Hashtags are #awesome!",
            ),
            (
                "Alice2",
                1,
                "M",
                "2022-01-01 12:05:00",
                "2022-01-01",
                "iPhone",
                "This is a #test tweet",
            ),
            (
                "Charlie",
                2,
                "M",
                "2022-01-01 12:00:00",
                "2022-01-01",
                "Android",
                "Love #pyspark",
            ),
            (
                "Charlie2",
                2,
                "M",
                "2022-01-01 12:05:00",
                "2022-01-01",
                "Android",
                "#DataEngineer is the future",
            ),
            ("David", 3, "M", "2022-01-01 12:00:00", "2022-01-01", "iPhone", ""),
            ("David2", 3, "M", "2022-01-01 12:15:00", "2022-01-01", "Android", ""),
            ("David3", 3, "M", "2022-01-01 12:20:00", "2022-01-01", "Android", ""),
            ("David", 3, "M", "2022-01-02 01:00:00", "2022-01-02", "Web", ""),
        ],
        schema=[
            "screen_name",
            "user_id",
            "gender",
            "created_ts",
            "tweet_date",
            "source",
            "text",
        ],
    )
    return df


@pytest.fixture(scope="session")
def tweet_pre_agg_test_df(spark: SparkSession) -> DataFrame:
    df = spark.createDataFrame(
        data=[
            (0, "Android", 1, "Bob", "2022-01-01 12:00:00", "2022-01-01", []),
            (
                1,
                "Android",
                1,
                "Alice2",
                "2022-01-01 12:00:00",
                "2022-01-01",
                ["#awesome"],
            ),
            (
                1,
                "iPhone",
                1,
                "Alice2",
                "2022-01-01 12:05:00",
                "2022-01-01",
                ["#awesome"],
            ),
            (
                2,
                "Android",
                2,
                "Charlie2",
                "2022-01-01 12:00:00",
                "2022-01-01",
                ["#twitter"],
            ),
            (
                2,
                "Android",
                2,
                "Charlie2",
                "2022-01-01 12:05:00",
                "2022-01-01",
                ["#awesome"],
            ),
            (
                3,
                "iPhone",
                1,
                "David3",
                "2022-01-01 12:00:00",
                "2022-01-01",
                ["#awesome"],
            ),
            (
                3,
                "Android",
                2,
                "David3",
                "2022-01-01 12:15:00",
                "2022-01-01",
                ["#awesome"],
            ),
            (
                3,
                "Android",
                2,
                "David3",
                "2022-01-01 12:20:00",
                "2022-01-01",
                ["#twitter"],
            ),
            (3, "Web", 1, "David", "2022-01-02 01:00:00", "2022-01-02", ["#twitter"]),
        ],
        schema=[
            "user_id",
            "source",
            "source_count",
            "screen_name",
            "created_ts",
            "tweet_date",
            "hashtags",
        ],
    )
    return df


@pytest.fixture(scope="session")
def tweet_quote_test_df(spark: SparkSession) -> DataFrame:
    df = spark.createDataFrame(
        data=[
            (True,),
            (True,),
            (False,),
            (False,),
        ],
        schema=["is_quote"],
    )
    return df
