# coding=gbk
from flask import Blueprint, jsonify, json
from flask import request
from ..Recommendation.Recommend import get_business_by_city

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

    df = get_business_by_city('New Orleans')

    df = df[df['name'].str.contains(query, case=False)]

    # 获取排序参数(可选)
    sortBy = request.args.get('sortBy')

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


    # 将排序后的数据帧转换为 JSON 格式
    json_res = df.to_json(orient='records')

    return json_res, 200

