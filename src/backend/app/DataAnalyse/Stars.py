
from flask import Blueprint
from sqlalchemy import text
from .SQLSession import get_session, toJSON, ToDataFrame
# 创建蓝图
stars_blue= Blueprint('stars', __name__,)


# 统计评分的分布情况
@stars_blue.route('/stars_count')
def stars_count():
    with get_session() as session:
        query = text("select * from stars_count")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计评分周（周一~周天）次数统计
@stars_blue.route('/stars_count_by_day_of_week')
def stars_count_by_day_of_week():
    with get_session() as session:
        query = text("select * from stars_count_by_day_of_week")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计拥有次数最多的5分评价的商家
@stars_blue.route('/business_with_most_5stars')
def business_with_most_5stars():
    with get_session() as session:
        query = text("select * from business_with_most_5stars")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res




