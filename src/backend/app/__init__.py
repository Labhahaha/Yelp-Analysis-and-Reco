from flask import Flask
from flask_cors import CORS
from pyspark.sql import SparkSession

from .SparkSessionBase import SparkSessionBase

app = Flask(__name__)
CORS(app)

# 配置应用程序
# app.config.from_object('config.Config')

# 创建 SparkSession
class YelpAnalysisJob(SparkSessionBase):
    SPARK_APP_NAME = "YelpAnalysisJob"
    SPARK_URL = "local"
    ENABLE_HIVE_SUPPORT = True
    def __init__(self):
        self.spark = self._create_spark_session()
        self.spark.sparkContext.setLogLevel("ERROR")


spark = YelpAnalysisJob().spark


# 注册蓝图
from .routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

