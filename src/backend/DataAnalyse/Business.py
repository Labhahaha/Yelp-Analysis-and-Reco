# coding:utf-8
from src.backend.DataAnalyse.SparkSessionBase import SparkSessionBase
from pyspark import HiveContext
from . import business_blue

class Business(SparkSessionBase):
    SPARK_URL = "local"
    SPARK_APP_NAME = 'BusinessJob'
    ENABLE_HIVE_SUPPORT = True
    def __init__(self):
        self.spark = self._create_spark_session()
        self.spark.sparkContext.setLogLevel("OFF")
        self.hc = HiveContext(self.spark.sparkContext)
        self.hc.sql('use yelp')
        self.business_table = self.hc.table('business')

    #找出美国最常见商户（前n）
    @business_blue.route('/search_most_business')
    def search_most_business(self,num=20):
        sql = f"SELECT name, COUNT(name) as name_count FROM business GROUP BY name ORDER BY name_count DESC LIMIT {num}"
        res= self.hc.sql(sql)
        return res

    #找出美国商户最多的城市
    def search_most_city(self,num=10):
        sql = f"SELECT city, COUNT(city) as city_count FROM business GROUP BY city ORDER BY city_count DESC LIMIT {num}"
        res= self.hc.sql(sql)
        return res

    #找出美国商户最多的州
    def search_most_state(self,num=5):
        sql = f"SELECT state, COUNT(state) as state_count FROM business GROUP BY state ORDER BY state_count DESC LIMIT {num}"
        res= self.hc.sql(sql)
        return res

    #找出美国最常见商户并显示平均评分
    def search_most_star(self,num=20):
        sql = f"SELECT name, AVG(stars) as avg_stars FROM business GROUP BY name ORDER BY COUNT(name) DESC LIMIT {num}"
        res = self.hc.sql(sql)
        return res

    # 关闭spark会话连接
    def close_session(self):
        self.spark.stop()



