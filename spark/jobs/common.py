import pyspark.sql.functions as F
import pyspark.sql.types as T

from pyspark.sql import DataFrame, SparkSession

from typing import Callable, NoReturn


def read_csv(spark: SparkSession, url: str, **kwargs) -> DataFrame:
    """spark read csv from url."""
    return spark.read.csv(url, **kwargs)

def write_to_database(df: DataFrame, url: str, table_name: str, **kwargs) -> NoReturn:
    """spark write dataframe to database"""
    (   df.write()
        .format()
        .option()
    )



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
    left: DataFrame, right: DataFrame, join_cond: Callable, *, join_type: str = "inner"
) -> DataFrame:
    df = left.join(right, join_cond(), join_type)
    return df


def parse_date_from_file_name() -> Callable:
    """returns function to parse date from file name"""

    return F.regexp_extract(F.input_file_name(), "\\d{4}-\\d{1,2}-\\d{1,2}", 0)


