from pyspark.sql import DataFrame, Column, SparkSession

scala_version = '2.13'
spark_version = '3.5.0'

packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    f'org.apache.kafka:kafka-clients:{spark_version}'
]


if __name__ == "__main__":

    # 1. connect
    # 2. with micro batch print to console
    spark = (
        SparkSession.builder
        .master("local") # type: ignore
        .appName(__file__)
        .config("spark.jars.packages", ",".join(packages))\
        .getOrCreate()
    )