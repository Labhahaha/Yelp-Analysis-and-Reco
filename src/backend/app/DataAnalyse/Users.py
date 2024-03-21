from flask import Blueprint
from sqlalchemy import text

from .SQLSession import get_session, toJSON

# 创建蓝图
users_blue = Blueprint('users', __name__, )


# 统计每年加入的用户数量
@users_blue.route('/user_count_by_registration_year')
def user_count_by_registration_year():
    with get_session() as session:
        query = text("select * from user_count_by_registration_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计评论达人
@users_blue.route('/user_with_most_review')
def user_with_most_review():
    with get_session() as session:
        query = text("select * from user_with_most_review")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计人气最高的用户
@users_blue.route('/user_with_most_fans')
def user_with_most_fans():
    with get_session() as session:
        query = text("select * from user_with_most_fans")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计每年优质用户、普通用户比例
@users_blue.route('/elite_user_ratio')
def elite_user_ratio():
    with get_session() as session:
        query = text("select * from elite_user_ratio")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 显示每年总用户数、沉默用户数（未写评论）的比例
@users_blue.route('/silent_user_ratio')
def silent_user_ratio():
    with get_session() as session:
        query = text("select * from silent_user_ratio")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计出每年的评论数
@users_blue.route('/review_count_bu_year')
def review_count_bu_year():
    with get_session() as session:
        query = text("select * from review_count_bu_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计出每年的精英用户
@users_blue.route('/elite_user_count_by_year')
def elite_user_count_by_year():
    with get_session() as session:
        query = text("select * from elite_user_count_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计出每年的tip数
@users_blue.route('/tip_count_by_year')
def tip_count_by_year():
    with get_session() as session:
        query = text("select * from tip_count_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计出每年的打卡数
@users_blue.route('/checkin_count_by_year')
def checkin_count_by_year():
    with get_session() as session:
        query = text("select * from checkin_count_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计出每年的综合数据
@users_blue.route('/info_by_year')
def info_by_year():
    with get_session() as session:
        query = text("select * from info_by_year")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res
