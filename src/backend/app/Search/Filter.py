# coding=gbk

from flask import Blueprint, jsonify, json
from flask import request
from numpy.core.defchararray import isdigit
from sqlalchemy import text
from ..utils.get_distance import cal_distance

from ..DataAnalyse.SQLSession import (get_session, toJSON, toDataFrame)

# 创建蓝图
filter_blue = Blueprint('filter', __name__)


global_df = None


# 按距离筛选商家
def filter_by_distance(filter_condition, user_location):
    global global_df
    with get_session() as session:
        query = text(f"select * from business where city = 'Affton' ")
        global_df = session.execute(query)
        global_df = toDataFrame(global_df)
    distance = global_df.apply(
                    lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]) / 1000, axis=1)
    print(distance)
    filter_df = global_df.assign(distance=distance)

    low = filter_condition[0]
    high = filter_condition[1]

    if isdigit(str(low)) and isdigit(str(high)):
        filter_df = filter_df[(filter_df["distance"] >= low) &
                              (filter_df["distance"] < high)]

    else:
        filter_df_ = None

    return filter_df


# 按星级评分筛选商家
def filter_by_stars(filter_condition):
    global global_df
    with get_session() as session:
        query = text(f"select * from business limit 10")
        global_df = session.execute(query)
        global_df = toDataFrame(global_df)
    # 五星商家
    if filter_condition == "five_stars":
        filter_df = global_df[global_df["stars"] == 5]

    # 四星及以上商家
    elif filter_condition == "more_than_four_stars":
        filter_df = global_df[global_df["stars"] >= 4]

    # 非法输入
    else:
        filter_df = None

    return filter_df


@filter_blue.route('/filter')
def myfilter():
    user_location = json.loads(request.args.get("user_location"))
    filter_type = request.args.get("filter_type")
    filter_condition = json.loads(request.args.get("filter_condition"))

    result = None
    if filter_type == "distance":
        result = filter_by_distance(filter_condition, user_location)
    elif filter_type == "stars":
        result = filter_by_stars(filter_condition)
    elif filter_type == "facilities":
        pass
    else:
        return None

    if result is None:
        return result
    # return jsonify(result_df), 200
    # result_df["business_id"].show(truncate=False)
    return result.to_json(orient='records')

