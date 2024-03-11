# coding=gbk
from flask import Blueprint, jsonify, json
from flask import request
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
        query = text(f"select * from business limit 200")
        global_df = session.execute(query)
        global_df = toDataFrame(global_df)
    distance = global_df.apply(lambda row: cal_distance(user_location, [row['longitude'], row['latitude']]), axis=1)
    filter_df = global_df.assign(distance=distance)
    # print(filter_df)
    # 不足1km
    if filter_condition == "(0,1)":
        filter_df = filter_df[(filter_df["distance"] >= 0) & (filter_df["distance"] < 1)]


    # 1~2km
    elif filter_condition == "(1,2)":
        filter_df = filter_df[(filter_df["distance"] >= 1) & (filter_df["distance"] < 2)]


    # 2~5km
    elif filter_condition == "(2,5)":
        filter_df = filter_df[(filter_df["distance"] >= 2) & (filter_df["distance"] < 5)]

    # 超过5km
    elif filter_condition == "(5,n)":
        filter_df = filter_df[filter_df["distance"] >=5]


    # 非法输入
    else:
        filter_df = None

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

    # 三星及以上商家
    elif filter_condition == "more_than_three_stars":
        filter_df = global_df[global_df["stars"] >= 3]

    # 非法输入
    else:
        filter_df = None

    return filter_df


@filter_blue.route('/filter')
def myfilter():
    user_location = json.loads(request.args.get("user_location"))
    filter_type = request.args.get("filter_type")
    filter_condition = request.args.get("filter_condition")

    result_df = None
    if filter_type == "distance":
        result_df = filter_by_distance(filter_condition, user_location)
    elif filter_type == "stars":
        result_df = filter_by_stars(filter_condition)
    elif filter_type == "facilities":
        pass
    else:
        pass
    # return jsonify(result_df), 200
    # result_df["business_id"].show(truncate=False)
    return result_df.to_json(orient='records')

