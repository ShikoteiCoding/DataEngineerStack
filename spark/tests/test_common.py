"""
Test commons
"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as T

from jobs.common import (
    read_csv,
    select_columns,
    attach_column,
    cast_column,
    group_dataframe,
)


def test_read_csv(spark: SparkSession, transaction_test_df: DataFrame):
    """test read of csv file"""
    url = "/tmp/transaction.csv"

    # Write dataframe to test reading
    transaction_test_df.write.mode("overwrite").csv(url, header=True)
    expected = [row for row in transaction_test_df.collect()]

    df = read_csv(spark, url, header=True, inferSchema=True)
    saved = [row for row in df.collect()]

    assert len(expected) == len(saved)
    for row in saved:
        assert set(row) in [set(row) for row in expected]


def test_select_columns(spark: SparkSession, transaction_test_df: DataFrame):
    """test column selections"""
    columns = transaction_test_df.columns
    selected_df = select_columns(transaction_test_df, columns)

    assert set(selected_df.columns) == set(columns)


def test_attach_column(spark: SparkSession, transaction_test_df: DataFrame):
    """test withColumn creation"""
    new_column_name = "double_amount"

    func = lambda: F.col("amount") * 2

    df_with_new_column = attach_column(transaction_test_df, new_column_name, func)

    assert df_with_new_column.count() == transaction_test_df.count()
    assert new_column_name in df_with_new_column.columns


def test_cast_column(spark: SparkSession, transaction_test_df: DataFrame):
    """test cast column type"""
    column_to_cast = "transaction_id"
    new_type = T.StringType()
    df_casted = cast_column(transaction_test_df, column_to_cast, new_type)

    assert df_casted.count() == transaction_test_df.count()
    assert df_casted.schema[column_to_cast].dataType == T.StringType()


def test_group_dataframe(spark: SparkSession, people_test_df: DataFrame):
    """test group dataframe by fields"""
    gender = lambda: ["gender"]
    count_and_age_mean = lambda: [
        F.count("name").alias("count"),
        F.avg("age").alias("avg_age"),
    ]
    grouped_df = group_dataframe(people_test_df, gender, count_and_age_mean)

    assert grouped_df.count() == 2
    assert set(grouped_df.columns) == set(["gender", "count", "avg_age"])
