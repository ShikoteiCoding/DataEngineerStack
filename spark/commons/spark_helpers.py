import pyspark.sql.functions as F

from pyspark.sql.types import DataType
from pyspark.sql import DataFrame, SparkSession, Column

from typing import Callable, Union


########################################################
################### Basic operations ###################
########################################################

def read_csv(spark: SparkSession, url: str, **kwargs) -> DataFrame:
    """spark read csv from url."""
    return spark.read.csv(url, **kwargs)


def select_columns(df: DataFrame, columns: Union[list[Column], list[str]]) -> DataFrame:
    return df.select(*columns)


def attach_column(df: DataFrame, column_name: str, func: Callable[[], Column]):
    df = df.withColumn(column_name, func())
    return df


def cast_column(df: DataFrame, column_name: str, _type: DataType, *, alias: str = ""):
    df = (
        df.withColumn(column_name, F.col(column_name).cast(_type))
        if not alias
        else df.withColumn(alias, F.col(column_name).cast(_type))
    )
    return df


def filter_dataframe(df: DataFrame, cond: Callable) -> DataFrame:
    df = df.filter(cond())
    return df


def group_dataframe(
    df: DataFrame, group_columns: list[Column], agg_columns: list[Column]
) -> DataFrame:
    df = df.groupBy(*group_columns).agg(*agg_columns)
    return df


def join_dataframe(
    left: DataFrame,
    right: DataFrame,
    join_cond: Callable[[], Column],
    *,
    join_type: str = "inner"
) -> DataFrame:
    df = left.join(right, join_cond(), join_type)
    return df


def parse_date_from_file_name() -> Column:
    """returns function to parse date from file name"""

    return F.regexp_extract(F.input_file_name(), "\\d{4}-\\d{1,2}-\\d{1,2}", 0)


########################################################
################## DataFrame handling ##################
########################################################
def remove_atomic_type(df: DataFrame, type_to_remove: DataType) -> DataFrame:
    ...