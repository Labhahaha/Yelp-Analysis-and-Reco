from pyspark import HiveContext
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType, FloatType, MapType

from src.backend.app import spark

# 定义 Hive 表的模式

# 定义用户表的模式
user_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("review_count", IntegerType(), True),
    StructField("yelping_since", StringType(), True),
    StructField("friends", ArrayType(StringType()), True),
    StructField("useful", IntegerType(), True),
    StructField("funny", IntegerType(), True),
    StructField("cool", IntegerType(), True),
    StructField("fans", IntegerType(), True),
    StructField("elite", ArrayType(StringType()), True),
    StructField("average_stars", FloatType(), True),
    StructField("compliment_hot", IntegerType(), True),
    StructField("compliment_more", IntegerType(), True),
    StructField("compliment_profile", IntegerType(), True),
    StructField("compliment_cute", IntegerType(), True),
    StructField("compliment_list", IntegerType(), True),
    StructField("compliment_note", IntegerType(), True),
    StructField("compliment_plain", IntegerType(), True),
    StructField("compliment_cool", IntegerType(), True),
    StructField("compliment_funny", IntegerType(), True),
    StructField("compliment_writer", IntegerType(), True),
    StructField("compliment_photos", IntegerType(), True)
])

# 定义商家表的模式
business_schema = StructType([
    StructField("business_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("postal_code", StringType(), True),
    StructField("latitude", FloatType(), True),
    StructField("longitude", FloatType(), True),
    StructField("stars", FloatType(), True),
    StructField("review_count", IntegerType(), True),
    StructField("is_open", IntegerType(), True),
    StructField("attributes", MapType(StringType(), StringType()), True),
    StructField("categories", ArrayType(StringType()), True),
    StructField("hours", MapType(StringType(), StringType()), True)
])

# 定义评论表的模式
review_schema = StructType([
    StructField("review_id", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("business_id", StringType(), True),
    StructField("stars", IntegerType(), True),
    StructField("date", StringType(), True),
    StructField("text", StringType(), True),
    StructField("useful", IntegerType(), True),
    StructField("funny", IntegerType(), True),
    StructField("cool", IntegerType(), True)
])

# 定义打卡表的模式
checkin_schema = StructType([
    StructField("business_id", StringType(), True),
    StructField("date", StringType(), True)
])

def get_users():
    # hive_context = HiveContext(spark.sparkContext)
    res = spark.sql("SELECT * FROM yelp.users")
    print(res)
    return res
    # return spark.table("users")

def create_user(user_data):
    df = spark.createDataFrame([user_data], schema=user_schema)
    df.write.mode("append").saveAsTable("users")

def get_businesses():
    return spark.table("businesses")

def create_business(business_data):
    df = spark.createDataFrame([business_data], schema=business_schema)
    df.write.mode("append").saveAsTable("businesses")

def get_reviews():
    return spark.table("reviews")

def create_review(review_data):
    df = spark.createDataFrame([review_data], schema=review_schema)
    df.write.mode("append").saveAsTable("reviews")

def get_checkins():
    return spark.table("checkins")

def create_checkin(checkin_data):
    df = spark.createDataFrame([checkin_data], schema=checkin_schema)
    df.write.mode("append").saveAsTable("checkins")