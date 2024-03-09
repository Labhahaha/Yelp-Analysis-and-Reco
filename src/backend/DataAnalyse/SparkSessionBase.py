# coding:utf-8
import os

from pyspark import SparkConf
from pyspark.sql import SparkSession


class SparkSessionBase:
    SPARK_APP_NAME = None
    SPARK_URL = "yarn"
    SPARK_EXECUTOR_MEMORY = "6g"
    SPARK_DRIVER_MEMORY = "4g"
    SPARK_EXECUTOR_CORES = 6
    SPARK_EXECUTOR_INSTANCES = 10
    ENABLE_HIVE_SUPPORT = False

    def _create_spark_session(self):
        if not os.environ.get('HADOOP_HOME'):
            os.environ['HADOOP_HOME'] = 'D:\\hadoop-2.7.7'

        if not os.environ.get('HADOOP_CONF_DIR'):
            os.environ['HADOOP_CONF_DIR'] = 'config/hadoop-conf'

        if not os.environ.get('YARN_CONF_DIR'):
            os.environ['YARN_CONF_DIR'] = 'config/yarn-conf'
        os.environ["HADOOP_USER_NAME"] = "asdf"
        conf = SparkConf()
        settings = (
            # 设置启动的spark的app名称，没有提供，将随机产生一个名称
            ("spark.app.name", self.SPARK_APP_NAME),
            # 设置该app启动时占用的内存用量，默认2g
            ("spark.executor.memory", self.SPARK_EXECUTOR_MEMORY),
            ("spark.driver.memory", self.SPARK_DRIVER_MEMORY),
            # spark master的地址
            ("spark.master", self.SPARK_URL),
            # 设置spark executor使用的CPU核心数，默认是1核心
            ("spark.executor.cores", self.SPARK_EXECUTOR_CORES),
            # 设置spark作业的Executor数量，默认为两个
            ("spark.executor.instances", self.SPARK_EXECUTOR_INSTANCES)
        )

        conf.setAll(settings)

        if self.ENABLE_HIVE_SUPPORT:
            return SparkSession.builder.config(conf=conf).enableHiveSupport().getOrCreate()
        else:
            return SparkSession.builder.config(conf=conf).getOrCreate()