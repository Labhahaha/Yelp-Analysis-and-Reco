from flask import Blueprint, jsonify, json
from flask import request
from .Filter import filter
from ..Recommendation.Recommend import get_recommendations
from .Order import sort
import pandas as pd
# 创建搜索蓝图
search_blue = Blueprint('search', __name__, )

@search_blue.route('/')
def search():
    # 获取搜索文本参数
    query = request.args.get('query')
    # 获取排序和筛选相关参数
    sortBy = request.args.get('sortBy')
    filter_type = request.args.get('filter_type')
    filter_condition = request.args.get("filter_condition")

    # 若无查询文本则返回缺失参数
    if query is None:
        return jsonify({"error": "Missing query parameter"}), 400

    # 调用推荐算法，实现基于搜索的推荐
    recommend_df = pd.read_json(get_recommendations(query),orient='records')

    # 根据条件进行排序
    if sort is not None:
        recommend_df = sort(recommend_df, sortBy)

    # 根据条件进行排序
    if filter_type is not None and filter_condition is not None:
        recommend_df = filter(recommend_df, filter_type, filter_condition)

    # 返回最终搜索结果
    json_res = recommend_df.to_json(orient='records')
    return json_res
