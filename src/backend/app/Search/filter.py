# coding=gbk
from flask import Blueprint, jsonify, json
from flask import request
from sqlalchemy import text
from ..utils.get_distance import cal_distance

from ..DataAnalyse.SQLSession import (get_session, toJSON, toDataFrame)

# ������ͼ
filter_blue = Blueprint('filter', __name__)


global_df = None


# ������ɸѡ�̼�
def filter_by_distance(filter_condition, user_location):
    global global_df
    with get_session() as session:
        query = text(f"select * from business limit 200")
        global_df = session.execute(query)
        global_df = toDataFrame(global_df)
    # ����1km
    if filter_condition == "(0,1)":
        filter_df = global_df[0 <= cal_distance(user_location, \
                    [global_df["longitude"], global_df["latitude"]]) < 1]

    # 1~2km
    elif filter_condition == "(1,2)":
        filter_df = global_df[1 <= cal_distance(user_location, \
                    [global_df["longitude"], global_df["latitude"]]) < 2]

    # 2~5km
    elif filter_condition == "(2,5)":
        filter_df = global_df[2 <= cal_distance(user_location, \
                    [global_df["longitude"], global_df["latitude"]]) < 5]

    # ����5km
    elif filter_condition == "(5,n)":
        filter_df = global_df[cal_distance(user_location, \
                    [global_df["longitude"], global_df["latitude"]]) >= 5]

    # �Ƿ�����
    else:
        filter_df = None

    return filter_df


# ���Ǽ�����ɸѡ�̼�
def filter_by_stars(filter_condition):
    global global_df
    with get_session() as session:
        query = text(f"select * from business limit 10")
        global_df = session.execute(query)
        global_df = toDataFrame(global_df)
    # �����̼�
    if filter_condition == "five_stars":
        filter_df = global_df[global_df["stars"] == 5]

    # ���Ǽ������̼�
    elif filter_condition == "more_than_four_stars":
        filter_df = global_df[global_df["stars"] >= 4]

    # ���Ǽ������̼�
    elif filter_condition == "more_than_three_stars":
        filter_df = global_df[global_df["stars"] >= 3]

    # �Ƿ�����
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

