from flask import Blueprint
from sqlalchemy import text

from .SQLSession import get_session, toJSON

# 创建蓝图
business_blue = Blueprint('business', __name__, )


# 找出美国最常见商户（前n）
@business_blue.route('/most_common_business')
def most_common_business():
    with get_session() as session:
        query = text("select * from most_common_business")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 找出美国商户最多的城市
@business_blue.route('/city_with_most_business')
def city_with_most_business():
    with get_session() as session:
        query = text("select * from city_with_most_business")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 找出美国商户最多的州
@business_blue.route('/state_with_most_business')
def state_with_most_business():
    with get_session() as session:
        query = text("select * from state_with_most_business")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 找出美国最常见商户并显示平均评分
@business_blue.route('/most_common_business_with_stars')
def most_common_business_with_stars():
    with get_session() as session:
        query = text("select * from most_common_business_with_stars")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计评分最高的城市（前10）
@business_blue.route('/highest_stars_city')
def highest_stars_city():
    with get_session() as session:
        query = text("select * from highest_stars_city")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计category的数量
@business_blue.route('/category_count')
def category_count():
    with get_session() as session:
        query = text("select * from category_count")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计商户数量最多的前十个category
@business_blue.route('/category_with_most_business')
def category_with_most_business():
    with get_session() as session:
        query = text("select * from category_with_most_business")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 收获五星评论最多的商户（前20）
@business_blue.route('/business_with_most_5stars')
def business_with_most_5stars():
    with get_session() as session:
        query = text("select * from business_with_most_5stars")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计不同类型的餐厅的数量
@business_blue.route('/different_types_restaurant_count')
def different_types_restaurant_count():
    with get_session() as session:
        query = text("select * from different_types_restaurant_count")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计不同类型的餐厅的评论数量
@business_blue.route('/different_types_restaurant_review_count')
def different_types_restaurant_review_count():
    with get_session() as session:
        query = text("select * from different_types_restaurant_review_count")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 统计不同类型的餐厅的评分分布
@business_blue.route('/different_types_restaurant_stars')
def different_types_restaurant_stars():
    with get_session() as session:
        query = text("select * from different_types_restaurant_stars")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res
