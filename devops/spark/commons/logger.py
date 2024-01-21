from pyspark.sql import SparkSession
from typing import Optional


class LoggerProvider:
    # TODO: not clean and force the use of a class for no reasons
    def get_logger(self, spark: SparkSession, custom_prefix: Optional[str] = ""):
        log4j_logger = spark._jvm.org.apache.log4j  # type: ignore
        return log4j_logger.LogManager.getLogger(custom_prefix + self.__full_name__())  # type: ignore

    def __full_name__(self):
        klass = self.__class__
        module = klass.__module__
        if module == "__builtin__":
            return klass.__name__
        return module + "." + klass.__name__
