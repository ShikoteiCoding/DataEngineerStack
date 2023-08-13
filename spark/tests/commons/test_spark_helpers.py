"""
Test commons
"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
import pyspark.sql.types as T

from commons.spark_helpers import (
    read_csv,
    select_columns,
    attach_column,
    cast_column,
    filter_dataframe,
    group_dataframe,
    join_dataframe,
    parse_date_from_file_name,
)


class TestBasicOperations:
    def test_read_csv(self, spark: SparkSession, transaction_test_df: DataFrame):
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

    def test_select_columns(self, spark: SparkSession, transaction_test_df: DataFrame):
        """test column selections"""
        columns = transaction_test_df.columns
        selected_df = select_columns(transaction_test_df, columns)

        assert set(selected_df.columns) == set(columns)

    def test_attach_column(self, spark: SparkSession, transaction_test_df: DataFrame):
        """test withColumn creation"""
        new_column_name = "double_amount"

        func = lambda: F.col("amount") * 2

        df_with_new_column = attach_column(transaction_test_df, new_column_name, func)

        assert df_with_new_column.count() == transaction_test_df.count()
        assert new_column_name in df_with_new_column.columns

    def test_cast_column(self, spark: SparkSession, transaction_test_df: DataFrame):
        """test cast column type"""
        column_to_cast = "transaction_id"
        new_type = T.StringType()
        df_casted = cast_column(transaction_test_df, column_to_cast, new_type)

        assert df_casted.count() == transaction_test_df.count()
        assert df_casted.schema[column_to_cast].dataType == T.StringType()

    def test_cast_column_with_alias(
        self, spark: SparkSession, transaction_test_df: DataFrame
    ):
        """test cast column type when target column name (alias)"""
        column_to_cast = "transaction_id"
        df_casted_integer = cast_column(
            transaction_test_df, column_to_cast, T.IntegerType()
        )
        df_casted_string = cast_column(
            df_casted_integer, column_to_cast, T.StringType(), alias="id"
        )

        assert df_casted_string.count() == transaction_test_df.count()
        assert df_casted_string.schema[column_to_cast].dataType == T.IntegerType()
        assert df_casted_string.schema["id"].dataType == T.StringType()

    def test_filter_dataframe(
        self, spark: SparkSession, transaction_test_df: DataFrame
    ):
        """test filter dataframe"""
        id_cond = lambda: (F.col("transaction_id") == 1)
        filtered_df = filter_dataframe(transaction_test_df, id_cond)

        assert filtered_df.count() == 1

    def test_group_dataframe(self, spark: SparkSession, people_test_df: DataFrame):
        """test group dataframe by fields"""
        gender = [F.col("gender")]
        count_and_age_mean = [
            F.count("name").alias("count"),
            F.avg("age").alias("avg_age"),
        ]
        grouped_df = group_dataframe(people_test_df, gender, count_and_age_mean)

        assert grouped_df.count() == 2
        assert set(grouped_df.columns) == set(["gender", "count", "avg_age"])

    def test_join_dataframe(self, spark: SparkSession, transaction_test_df: DataFrame):
        """test filter dataframe"""
        cond = lambda: (F.col("left.transaction_id") == F.col("right.transaction_id"))

        joined_df = join_dataframe(
            transaction_test_df.alias("left"),
            transaction_test_df.alias("right"),
            cond,
            join_type="inner",
        )

        assert set(joined_df.columns) == set(transaction_test_df.columns)
        assert joined_df.count() == 2

    def test_parse_date_from_file_name(
        self, spark: SparkSession, transaction_test_df: DataFrame
    ):
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
            output
            == spark.createDataFrame(expected_output, ["input_file_date"]).collect()
        )

    def test_parse_date_from_file_name_without_date(
        self, spark: SparkSession, transaction_test_df: DataFrame
    ):
        """test read of csv without date filename to extract"""
        url = "/tmp/file.csv"

        # write dataframe with specific filename
        transaction_test_df.write.mode("overwrite").csv(url, header=True)

        # read the temporary stored DataFrame
        df = read_csv(spark, url, header=True, inferSchema=True)

        # apply the function to the DataFrame
        output = (
            attach_column(df, "input_file_date", parse_date_from_file_name)
            .select("input_file_date")
            .collect()
        )

        expected_output = [
            ("",),
            ("",),
        ]

        assert (
            output
            == spark.createDataFrame(expected_output, ["input_file_date"]).collect()
        )


class TestRemoveDataTypeFromDF:
    ...
