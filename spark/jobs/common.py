import pyspark.sql.functions as F
import pyspark.sql.types as T

from pyspark.sql import DataFrame, SparkSession

from typing import Callable


def read_csv(spark: SparkSession, url: str, **kwargs) -> DataFrame:
    return spark.read.csv(url, **kwargs)


def select_columns(df: DataFrame, columns=list[str]) -> DataFrame:
    return df.select(columns)


def attach_column(df: DataFrame, column_name: str, func: Callable):
    df = df.withColumn(column_name, func())
    return df


def cast_column(df: DataFrame, column_name: str, _type: T, *, alias: str = ""):
    df = (
        df.withColumn(column_name, F.col(column_name).cast(_type))
        if not alias
        else df.withColumn(alias, F.col(column_name).cast(_type))
    )
    return df


def filter_dataframe(df: DataFrame, cond: Callable) -> DataFrame:
    df = df.filter(cond())
    return df


def group_dataframe(df: DataFrame, columns: Callable, agg_funcs: Callable) -> DataFrame:
    df = df.groupBy(*columns()).agg(*agg_funcs())
    return df


def join_dataframe(
    left: DataFrame,
    right: DataFrame,
    join_cond: Callable,
    *,
    join_type: str = "inner",
    left_alias: str = "",
    right_alias: str = ""
) -> DataFrame:
    left = left if not left_alias else left.alias(left_alias)
    right = right if not right_alias else right.alias(right_alias)
    df = left.join(right, join_cond(), join_type)
    return df
