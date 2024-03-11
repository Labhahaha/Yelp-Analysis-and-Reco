#coding=gbk
from math import radians, cos, sin, asin, sqrt

from sqlalchemy import text

from ..DataAnalyse.SQLSession import get_session


def get_distance_fromSQL(user_location,business_id):
    # ��ȡ�û��ľ�γ��
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
    # ��ȡ�û��ľ�γ��
    user_longitude = user_location[0]
    user_latitude = user_location[1]
    business_longitude = business_location[0]
    business_latitude = business_location[1]

    return haversine(user_longitude, user_latitude, business_longitude, business_latitude)

def haversine(lon1, lat1, lon2, lat2):
    """
    ����������γ������֮���ʵ�ʾ��루��λ���ף�

    :param lon1: ��һ����ľ��ȣ���λ���ȣ�
    :param lat1: ��һ�����γ�ȣ���λ���ȣ�
    :param lon2: �ڶ�����ľ��ȣ���λ���ȣ�
    :param lat2: �ڶ������γ�ȣ���λ���ȣ�
    :return: ����֮���ʵ�ʾ��루��λ���ף�
    """
    # ��ʮ���ƶ���ת��Ϊ����
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine��ʽ
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # ����ƽ���뾶����λ��ǧ�ף�
    return c * r * 1000  # ת��Ϊ��