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
    star_condition = request.args.get('star_condition')
    distance_condition = request.args.get('distance_condition')

    # 调用推荐算法，实现基于搜索的推荐
    recommend_df = pd.read_json(get_recommendations(),orient='records')

    # 根据条件进行排序
    if sortBy is not None and sortBy != '':
        recommend_df = sort(recommend_df, sortBy)

    # 处理筛选条件
    filter_conditions = {}

    if star_condition and star_condition != '':
        filter_conditions['stars'] = star_condition
    if distance_condition and distance_condition != '':
        filter_conditions['distance'] = distance_condition

    # 根据条件进行排序
    recommend_df = filter(recommend_df, filter_conditions)

    # 返回最终搜索结果
    json_res = recommend_df.to_json(orient='records')
    return json_res
