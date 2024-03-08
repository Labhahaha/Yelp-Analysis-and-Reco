from SparkSessionBase import SparkSessionBase


class TextRandJob(SparkSessionBase):
    SPARK_URL = "local"
    SPARK_APP_NAME = 'TextRandJob'
    ENABLE_HIVE_SUPPORT = True

    def __init__(self):
        self.spark = self._create_spark_session()
        self.spark.sparkContext.setLogLevel("ERROR")

    def start(self):
        res = self.spark.sql("SELECT * FROM yelp.checkin limit 10")
        res.show()
        return res


if __name__ == '__main__':
    TextRandJob().start()
