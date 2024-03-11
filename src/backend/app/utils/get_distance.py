#coding=gbk
from math import radians, cos, sin, asin, sqrt

from sqlalchemy import text

from ..DataAnalyse.SQLSession import get_session


def get_distance_fromSQL(user_location,business_id):
    # 获取用户的经纬度
    user_longitude = user_location[0]
    user_latitude = user_location[1]

    business_longitude = 0
    business_latitude = 0

    with get_session() as session:
        query = text("select longitude,latitude from business where business_id = :business_id")
        res = session.execute(query, {"business_id": business_id})
        for row in res:
            business_longitude = row[0]
            business_latitude = row[1]

    return haversine(user_longitude, user_latitude, business_longitude, business_latitude)

def get_distance(user_location,business_location):
    # 获取用户的经纬度
    user_longitude = user_location[0]
    user_latitude = user_location[1]
    business_longitude = business_location[0]
    business_latitude = business_location[1]

    return haversine(user_longitude, user_latitude, business_longitude, business_latitude)

def haversine(lon1, lat1, lon2, lat2):
    """
    计算两个经纬度坐标之间的实际距离（单位：米）

    :param lon1: 第一个点的经度（单位：度）
    :param lat1: 第一个点的纬度（单位：度）
    :param lon2: 第二个点的经度（单位：度）
    :param lat2: 第二个点的纬度（单位：度）
    :return: 两点之间的实际距离（单位：米）
    """
    # 将十进制度数转换为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径（单位：千米）
    return c * r * 1000  # 转换为米