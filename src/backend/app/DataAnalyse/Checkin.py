from flask import Blueprint
from sqlalchemy import text

from .SQLSession import get_session, toJSON

# 创建蓝图
checkin_blue = Blueprint('checkin', __name__, )


# 统计每年的打卡次数
@checkin_blue.route('/checkin_count_by_year')
def checkin_count_by_year():
    with get_session() as session:
        query = text("select * from checkin_count_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计24小时每小时打卡次数
@checkin_blue.route('/checkin_count_by_hour')
def checkin_count_by_hour():
    with get_session() as session:
        query = text("select * from checkin_count_by_hour")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计最喜欢打卡的城市
@checkin_blue.route('/city_with_most_checkin')
def city_with_most_checkin():
    with get_session() as session:
        query = text("select * from city_with_most_checkin")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 全部商家的打卡排行榜
@checkin_blue.route('/business_order_by_checkin_count')
def business_order_by_checkin_count():
    with get_session() as session:
        query = text("select * from business_order_by_checkin_count")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res
