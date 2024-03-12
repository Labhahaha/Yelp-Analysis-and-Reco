# coding=gbk
from flask import Blueprint, jsonify, json
from flask import request
from ..utils import get_business_by_city, cal_distance
from .Filter import filter

# 创建蓝图
search_blue = Blueprint('search', __name__, )

df=None

# 获取商户详情
@search_blue.route('/')
def search():
    # 获取查询参数
    query = request.args.get('query')
    if query is None:
        return jsonify({"error": "Missing query parameter"}), 400

    # 按城市获取商家数据
    df = get_business_by_city('Abington')

    # 计算用户与每一个商家的距离，df中新增distance列
    df['distance'] = df.apply(lambda row: cal_distance([-75.111,40.1282], [row['longitude'], row['latitude']]), axis=1)

    # 进行模糊查询
    df = df[df['name'].str.contains(query, case=False)]

    # 获取排序参数(可选)
    sortBy = request.args.get('sortBy')

    # 进行排序(可选)
    if sortBy == 'stars':
        # 按照星级从高到低排序
        df = df.sort_values(by='stars', ascending=False)

    if sortBy == 'review_count':
        # 按照评论数量从高到低排序
        df = df.sort_values(by='review_count', ascending=False)
        print(df)

    if sortBy == 'distance':
        # 按照距离从近到远排序
        df = df.sort_values(by='distance')

    # 获取筛选参数(可选)
    filter_type = request.args.get('filter')
    filter_condition = request.args.get("filter_condition")

    # 进行筛选(可选)
    df=filter(df,filter_type,filter_condition)


    # 将排序/筛选后的数据转换为 JSON 格式
    json_res = df.to_json(orient='records')

    return json_res, 200

