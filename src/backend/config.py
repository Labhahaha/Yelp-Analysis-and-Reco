# import os
#
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#
# class Config:
#     SPARK_APP_NAME = 'test'
#     SPARK_MASTER = "172.16.0.245"  # 或者指定 Spark 集群的 master URL
#     HIVE_METASTORE_URI = "thrift://172.16.0.247:9083"  # 替换为你的 Hive Metastore URI
#     SPARK_URL = "local"
#     ENABLE_HIVE_SUPPORT = True
#
#     # 添加其他配置项...